from fastapi.testclient import TestClient

from main import app

cliente = TestClient(app)


def test_mesmo_assento_duas_vezes_da_409():
    pedido = {"evento": 1, "assento": "Z-99"}
    primeira = cliente.post("/reservas", json=pedido)
    segunda = cliente.post("/reservas", json=pedido)
    assert primeira.status_code == 201
    assert segunda.status_code == 409
