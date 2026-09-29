"""Estas pruebas deben pasar antes de iniciar y conservarse en la entrega."""


def test_health(client):
    assert client.get('/health').json() == {'status': 'ok'}


def test_listado_vacio(client):
    response = client.get('/pedidos')
    assert response.status_code == 200
    assert response.json() == []


def test_crear_y_consultar(client):
    response = client.post('/pedidos', json={'cliente': 'Demo', 'descripcion': 'Entrega ficticia'})
    assert response.status_code == 201
    pedido = response.json()
    assert pedido['estado'] == 'pendiente'
    assert client.get(f"/pedidos/{pedido['id']}").json() == pedido


def test_pedido_inexistente(client):
    assert client.get('/pedidos/999999').status_code == 404
