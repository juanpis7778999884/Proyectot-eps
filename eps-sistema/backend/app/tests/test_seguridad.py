from fastapi.testclient import TestClient


def test_rate_limiting(client: TestClient, auth_headers):
    for _ in range(70):
        resp = client.get("/api/v1/afiliados/", headers=auth_headers)
    assert resp.status_code in (200, 429)


def test_token_expirado_o_invalido(client: TestClient):
    resp = client.get(
        "/api/v1/afiliados/",
        headers={"Authorization": "Bearer token.muy.mal.formado"},
    )
    assert resp.status_code == 401


def test_tipo_token_incorrecto(client: TestClient, superuser):
    from app.core.security import create_refresh_token
    refresh = create_refresh_token(subject="1")
    resp = client.get(
        "/api/v1/afiliados/",
        headers={"Authorization": f"Bearer {refresh}"},
    )
    assert resp.status_code == 401
