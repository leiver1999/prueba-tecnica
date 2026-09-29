"""P2: comprobar el filtro HTTP contra una base SQLite temporal."""
import pytest
from app.db import connection


@pytest.fixture
def pedidos_variados(client):
    # P3 aun no esta implementado: preparar los estados directamente en la base de prueba.
    with connection(client.app.state.db_path) as conn:
        conn.executemany(
            'INSERT INTO pedidos (cliente, descripcion, estado) VALUES (?, ?, ?)',
            [
                ('Demo A', 'Entrega A', 'pendiente'),
                ('Demo B', 'Entrega B', 'en_proceso'),
                ('Demo C', 'Entrega C', 'completado'),
                ('Demo D', 'Entrega D', 'pendiente'),
            ],
        )


@pytest.mark.parametrize('estado, ids', [
    ('pendiente', [1, 4]),
    ('en_proceso', [2]),
    ('completado', [3]),
])
def test_filtrar_por_estado(client, pedidos_variados, estado, ids):
    response = client.get('/pedidos', params={'estado': estado})
    assert response.status_code == 200
    pedidos = response.json()
    assert [pedido['id'] for pedido in pedidos] == ids
    assert all(pedido['estado'] == estado for pedido in pedidos)


def test_sin_filtro_devuelve_todos(client, pedidos_variados):
    response = client.get('/pedidos')
    assert response.status_code == 200
    assert [pedido['id'] for pedido in response.json()] == [1, 2, 3, 4]


@pytest.mark.parametrize('estado', ['', 'inventado', ' ', 'Pendiente', "pendiente' OR 1=1 --"])
def test_estado_invalido_no_modifica_datos(client, pedidos_variados, estado):
    antes = client.get('/pedidos').json()
    response = client.get('/pedidos', params={'estado': estado})
    assert response.status_code == 400
    assert isinstance(response.json()['detail'], str)
    assert response.json()['detail']
    assert client.get('/pedidos').json() == antes


def test_filtro_sin_coincidencias(client):
    creado = client.post('/pedidos', json={'cliente': 'Demo', 'descripcion': 'Entrega'})
    assert creado.status_code == 201
    response = client.get('/pedidos', params={'estado': 'completado'})
    assert response.status_code == 200
    assert response.json() == []
