from fastapi.testclient import TestClient


def test_crear_cita(client: TestClient, auth_headers, afiliado_principal, medico_principal):
    resp = client.post(
        "/api/v1/citas/",
        json={
            "afiliado_id": afiliado_principal.id,
            "medico_id": medico_principal.id,
            "fecha_hora": "2026-12-01T10:00:00",
            "motivo": "Consulta general",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["estado"] == "agendada"


def test_cita_conflicto_horario(client: TestClient, auth_headers, afiliado_principal, medico_principal):
    payload = {
        "afiliado_id": afiliado_principal.id,
        "medico_id": medico_principal.id,
        "fecha_hora": "2026-12-01T10:00:00",
        "motivo": "Duplicada",
    }
    client.post("/api/v1/citas/", json=payload, headers=auth_headers)
    resp = client.post("/api/v1/citas/", json=payload, headers=auth_headers)
    assert resp.status_code == 400


def test_listar_citas(client: TestClient, auth_headers):
    resp = client.get("/api/v1/citas/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_obtener_cita_inexistente(client: TestClient, auth_headers):
    resp = client.get("/api/v1/citas/999999", headers=auth_headers)
    assert resp.status_code == 404


def test_actualizar_cita(client: TestClient, auth_headers, afiliado_principal, medico_principal):
    resp = client.post(
        "/api/v1/citas/",
        json={
            "afiliado_id": afiliado_principal.id,
            "medico_id": medico_principal.id,
            "fecha_hora": "2026-12-02T10:00:00",
            "motivo": "Original",
        },
        headers=auth_headers,
    )
    cita_id = resp.json()["id"]
    resp2 = client.put(
        f"/api/v1/citas/{cita_id}",
        json={"motivo": "Control"},
        headers=auth_headers,
    )
    assert resp2.status_code == 200, resp2.text
    assert resp2.json()["motivo"] == "Control"


def test_cancelar_cita(client: TestClient, auth_headers, afiliado_principal, medico_principal):
    resp = client.post(
        "/api/v1/citas/",
        json={
            "afiliado_id": afiliado_principal.id,
            "medico_id": medico_principal.id,
            "fecha_hora": "2026-12-03T10:00:00",
            "motivo": "Para cancelar",
        },
        headers=auth_headers,
    )
    cita_id = resp.json()["id"]
    resp2 = client.delete(f"/api/v1/citas/{cita_id}", headers=auth_headers)
    assert resp2.status_code == 200, resp2.text
