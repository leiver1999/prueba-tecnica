"""P3: actualizar pedidos y comprobar errores y persistencia con SQLite temporal."""
import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def pedido(client):
    response = client.post('/pedidos', json={'cliente': 'Demo', 'descripcion': 'Entrega'})
    assert response.status_code == 201
    return response.json()


def test_actualizar_estado_conserva_campos_y_otros_pedidos(client, pedido):
    otro = client.post('/pedidos', json={'cliente': 'Otro', 'descripcion': 'Otra entrega'})
    assert otro.status_code == 201
    otro_pedido = otro.json()
    ruta = f"/pedidos/{pedido['id']}"

    for estado in ('en_proceso', 'completado', 'completado', 'pendiente'):
        response = client.patch(f'{ruta}/estado', json={'estado': estado})
        esperado = {**pedido, 'estado': estado}
        assert response.status_code == 200
        assert response.json() == esperado
        assert client.get(ruta).json() == esperado
        assert client.get(f"/pedidos/{otro_pedido['id']}").json() == otro_pedido
        filtrados = client.get('/pedidos', params={'estado': estado}).json()
        assert esperado in filtrados


@pytest.mark.parametrize('estado', ['', 'inventado', 'Pendiente', ' pendiente '])
def test_estado_invalido_no_actualiza(client, pedido, estado):
    antes = client.get('/pedidos').json()
    response = client.patch(f"/pedidos/{pedido['id']}/estado", json={'estado': estado})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Estado no valido'}
    assert client.get('/pedidos').json() == antes


def test_actualizar_id_inexistente_no_crea_pedido(client, pedido):
    antes = client.get('/pedidos').json()
    response = client.patch('/pedidos/999999/estado', json={'estado': 'completado'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Pedido no encontrado'}
    assert client.get('/pedidos').json() == antes


@pytest.mark.parametrize('payload', [
    {},
    {'estado': None},
    {'estado': 123},
    {'estado': []},
    {'estado': 'completado', 'extra': True},
])
def test_cuerpo_invalido_conserva_422_y_datos(client, pedido, payload):
    antes = client.get('/pedidos').json()
    response = client.patch(f"/pedidos/{pedido['id']}/estado", json=payload)
    assert response.status_code == 422
    assert client.get('/pedidos').json() == antes


def test_id_no_entero_conserva_422_y_datos(client, pedido):
    antes = client.get('/pedidos').json()
    response = client.patch('/pedidos/abc/estado', json={'estado': 'completado'})
    assert response.status_code == 422
    assert client.get('/pedidos').json() == antes


def test_estado_persiste_al_reabrir_aplicacion(tmp_path):
    db_path = tmp_path / 'persistencia.sqlite3'
    with TestClient(create_app(db_path)) as primera:
        creado = primera.post('/pedidos', json={'cliente': 'Demo', 'descripcion': 'Entrega'})
        assert creado.status_code == 201
        pedido = creado.json()
        response = primera.patch(
            f"/pedidos/{pedido['id']}/estado", json={'estado': 'completado'}
        )
        assert response.status_code == 200

    with TestClient(create_app(db_path)) as segunda:
        response = segunda.get(f"/pedidos/{pedido['id']}")
        assert response.status_code == 200
        assert response.json() == {**pedido, 'estado': 'completado'}
