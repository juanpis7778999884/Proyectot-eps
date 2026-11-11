from fastapi.testclient import TestClient


def test_crear_medico(client: TestClient, auth_headers):
    resp = client.post(
        "/api/v1/medicos/",
        json={
            "numero_licencia": "MED001",
            "nombre": "Carlos",
            "consultorio": "101",
            "telefono": "3001112222",
            "activo": True,
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["numero_licencia"] == "MED001"


def test_medico_licencia_duplicada(client: TestClient, auth_headers):
    payload = {
        "numero_licencia": "MED001",
        "nombre": "Carlos",
        "activo": True,
    }
    client.post("/api/v1/medicos/", json=payload, headers=auth_headers)
    resp = client.post("/api/v1/medicos/", json=payload, headers=auth_headers)
    assert resp.status_code == 400


def test_listar_medicos(client: TestClient, auth_headers):
    resp = client.get("/api/v1/medicos/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_crear_especialidad(client: TestClient, auth_headers):
    resp = client.post(
        "/api/v1/medicos/especialidades",
        json={"nombre": "Cardiología", "descripcion": "Corazón", "activo": True},
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text


def test_especialidad_duplicada(client: TestClient, auth_headers):
    client.post(
        "/api/v1/medicos/especialidades",
        json={"nombre": "Cardiología", "activo": True},
        headers=auth_headers,
    )
    resp = client.post(
        "/api/v1/medicos/especialidades",
        json={"nombre": "Cardiología", "activo": True},
        headers=auth_headers,
    )
    assert resp.status_code == 400
