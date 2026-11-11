from fastapi.testclient import TestClient


def test_crear_factura(client: TestClient, auth_headers, afiliado_principal):
    resp = client.post(
        "/api/v1/facturacion/",
        json={
            "afiliado_id": afiliado_principal.id,
            "monto": 50.0,
            "estado": "pendiente",
            "detalle": "Consulta médica",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["estado"] == "pendiente"


def test_listar_facturas(client: TestClient, auth_headers):
    resp = client.get("/api/v1/facturacion/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_actualizar_factura(client: TestClient, auth_headers, afiliado_principal):
    resp = client.post(
        "/api/v1/facturacion/",
        json={
            "afiliado_id": afiliado_principal.id,
            "monto": 30.0,
            "estado": "pendiente",
            "detalle": "Para pagar",
        },
        headers=auth_headers,
    )
    factura_id = resp.json()["id"]
    resp2 = client.patch(
        f"/api/v1/facturacion/{factura_id}",
        json={"estado": "pagada"},
        headers=auth_headers,
    )
    assert resp2.status_code == 200, resp2.text
    assert resp2.json()["estado"] == "pagada"


def test_factura_inexistente(client: TestClient, auth_headers):
    resp = client.get("/api/v1/facturacion/999999", headers=auth_headers)
    assert resp.status_code == 404
