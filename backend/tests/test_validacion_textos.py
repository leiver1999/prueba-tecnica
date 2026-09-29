"""P1/P4: normalizacion y rechazo de textos vacios con SQLite temporal."""
import pytest


def test_crear_recorta_extremos_y_guarda_textos_normalizados(client):
    response = client.post('/pedidos', json={
        'cliente': '  Cliente Demo  ',
        'descripcion': '\t  Entrega de  prueba  \n',
    })
    assert response.status_code == 201
    pedido = response.json()
    esperado = {
        'id': pedido['id'],
        'cliente': 'Cliente Demo',
        'descripcion': 'Entrega de  prueba',
        'estado': 'pendiente',
    }
    assert pedido == esperado

    consulta = client.get(f"/pedidos/{pedido['id']}")
    assert consulta.status_code == 200
    assert consulta.json() == esperado
    assert client.get('/pedidos').json() == [esperado]


@pytest.mark.parametrize('campo', ['cliente', 'descripcion'])
@pytest.mark.parametrize('texto', ['', '   ', '\t\n '])
def test_texto_vacio_no_inserta_ni_modifica_datos(client, campo, texto):
    existente = client.post('/pedidos', json={
        'cliente': 'Existente', 'descripcion': 'Conservar este pedido',
    })
    assert existente.status_code == 201
    antes = client.get('/pedidos').json()

    payload = {'cliente': 'Cliente Demo', 'descripcion': 'Entrega de prueba'}
    payload[campo] = texto
    response = client.post('/pedidos', json=payload)

    assert response.status_code == 400
    assert response.json() == {'detail': 'Cliente y descripcion no pueden estar vacios'}
    assert client.get('/pedidos').json() == antes


def test_ambos_textos_en_blanco_no_crean_pedido(client):
    response = client.post('/pedidos', json={'cliente': '   ', 'descripcion': '   '})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Cliente y descripcion no pueden estar vacios'}
    assert client.get('/pedidos').json() == []
