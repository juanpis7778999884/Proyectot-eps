from fastapi.testclient import TestClient


def test_listar_auditoria(client: TestClient, auth_headers):
    resp = client.get("/api/v1/auditoria/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_auditoria_sin_permisos(client: TestClient, db):
    from app.crud import user as crud_user
    from app.schemas import UserCreate
    from app.core.security import get_password_hash

    aux = crud_user.create(
        db,
        obj_in=UserCreate(
            email="aux2@test.com",
            full_name="Aux2",
            role="auxiliar",
            password="AuxPass123!",
            is_active=True,
        ),
    )
    aux.hashed_password = get_password_hash("AuxPass123!")
    db.add(aux)
    db.commit()

    resp = client.post(
        "/api/v1/auth/login",
        data={"email": "aux2@test.com", "password": "AuxPass123!"},
    )
    aux_token = resp.json()["access_token"]

    resp2 = client.get(
        "/api/v1/auditoria/",
        headers={"Authorization": f"Bearer {aux_token}"},
    )
    assert resp2.status_code == 403
