from fastapi.testclient import TestClient


def test_crear_afiliado(client: TestClient, auth_headers):
    resp = client.post(
        "/api/v1/afiliados/",
        json={
            "tipo_documento": "CC",
            "numero_documento": "12345678",
            "nombre": "Juan",
            "apellido": "Pérez",
            "fecha_nacimiento": "1990-01-01T00:00:00",
            "genero": "M",
            "email": "juan@test.com",
            "telefono": "3000000000",
            "direccion": "Calle 1",
            "plan": "contributivo",
            "estado": "activo",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["numero_documento"] == "12345678"


def test_afiliado_documento_duplicado(client: TestClient, auth_headers):
    payload = {
        "tipo_documento": "CC",
        "numero_documento": "12345678",
        "nombre": "Juan",
        "apellido": "Pérez",
        "plan": "contributivo",
        "estado": "activo",
    }
    client.post("/api/v1/afiliados/", json=payload, headers=auth_headers)
    resp = client.post("/api/v1/afiliados/", json=payload, headers=auth_headers)
    assert resp.status_code == 400


def test_listar_afiliados(client: TestClient, auth_headers):
    resp = client.get("/api/v1/afiliados/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_obtener_afiliado_inexistente(client: TestClient, auth_headers):
    resp = client.get("/api/v1/afiliados/999999", headers=auth_headers)
    assert resp.status_code == 404


def test_actualizar_afiliado(client: TestClient, auth_headers, afiliado_principal):
    resp = client.put(
        f"/api/v1/afiliados/{afiliado_principal.id}",
        json={"telefono": "3100000000"},
        headers=auth_headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["telefono"] == "3100000000"


def test_eliminar_afiliado(client: TestClient, auth_headers):
    resp = client.post(
        "/api/v1/afiliados/",
        json={
            "tipo_documento": "CC",
            "numero_documento": "87654321",
            "nombre": "Ana",
            "apellido": "Gómez",
            "plan": "contributivo",
            "estado": "activo",
        },
        headers=auth_headers,
    )
    afiliado_id = resp.json()["id"]
    resp2 = client.delete(f"/api/v1/afiliados/{afiliado_id}", headers=auth_headers)
    assert resp2.status_code == 200, resp2.text


def test_sin_token_afiliados(client: TestClient):
    resp = client.get("/api/v1/afiliados/")
    assert resp.status_code == 401
