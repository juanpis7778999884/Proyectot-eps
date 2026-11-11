from fastapi.testclient import TestClient


def test_crear_orden(client: TestClient, auth_headers, afiliado_principal, medico_principal):
    resp = client.post(
        "/api/v1/ordenes/",
        json={
            "afiliado_id": afiliado_principal.id,
            "medico_id": medico_principal.id,
            "tipo": "procedimiento",
            "detalle": "Rayos X tórax",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["estado"] == "solicitada"


def test_autorizar_orden(client: TestClient, auth_headers, afiliado_principal, medico_principal):
    resp = client.post(
        "/api/v1/ordenes/",
        json={
            "afiliado_id": afiliado_principal.id,
            "medico_id": medico_principal.id,
            "tipo": "procedimiento",
            "detalle": "Para autorizar",
        },
        headers=auth_headers,
    )
    orden_id = resp.json()["id"]
    resp2 = client.patch(
        f"/api/v1/ordenes/{orden_id}",
        json={"estado": "autorizada"},
        headers=auth_headers,
    )
    assert resp2.status_code == 200, resp2.text
    assert resp2.json()["estado"] == "autorizada"


def test_listar_ordenes(client: TestClient, auth_headers):
    resp = client.get("/api/v1/ordenes/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_orden_inexistente(client: TestClient, auth_headers):
    resp = client.get("/api/v1/ordenes/999999", headers=auth_headers)
    assert resp.status_code == 404
