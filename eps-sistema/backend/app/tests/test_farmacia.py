from fastapi.testclient import TestClient


def test_crear_medicamento(client: TestClient, auth_headers):
    resp = client.post(
        "/api/v1/farmacia/medicamentos",
        json={
            "nombre": "Paracetamol",
            "principio_activo": "Paracetamol",
            "concentracion": "500mg",
            "laboratorio": "LabX",
            "precio_unitario": 2.5,
            "stock": 100,
            "activo": True,
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["stock"] == 100


def test_listar_medicamentos(client: TestClient, auth_headers):
    resp = client.get("/api/v1/farmacia/medicamentos", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_crear_dispensacion(client: TestClient, auth_headers, db):
    from app.models.farmacia import Medicamento
    m = db.get(Medicamento, 1)
    if m is None:
        m = Medicamento(nombre="Ibuprofeno", stock=50, precio_unitario=3.0)
        db.add(m)
        db.commit()
        db.refresh(m)

    resp = client.post(
        "/api/v1/farmacia/dispensaciones",
        json={
            "medicamento_id": m.id,
            "farmaceutico_id": 1,
            "cantidad": 10,
            "observaciones": "Entregado",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text


def test_dispensacion_stock_insuficiente(client: TestClient, auth_headers, db):
    from app.models.farmacia import Medicamento
    m = db.get(Medicamento, 1)
    if m is None:
        m = Medicamento(nombre="Stock Bajo", stock=1, precio_unitario=1.0)
        db.add(m)
        db.commit()
        db.refresh(m)
    resp = client.post(
        "/api/v1/farmacia/dispensaciones",
        json={
            "medicamento_id": m.id,
            "farmaceutico_id": 1,
            "cantidad": 999999,
        },
        headers=auth_headers,
    )
    assert resp.status_code == 400


def test_medicamento_inexistente(client: TestClient, auth_headers):
    resp = client.patch(
        "/api/v1/farmacia/medicamentos/999999",
        json={"stock": 5},
        headers=auth_headers,
    )
    assert resp.status_code == 404
