from fastapi.testclient import TestClient


def test_registro_sin_permisos(client: TestClient, db):
    from app.crud import user as crud_user
    from app.schemas import UserCreate
    from app.core.security import get_password_hash

    aux = crud_user.create(
        db,
        obj_in=UserCreate(
            email="aux3@test.com",
            full_name="Aux Tres",
            role="auxiliar",
            password="AuxPass123!",
            is_active=True,
        ),
    )
    db.commit()
    resp = client.post(
        "/api/v1/auth/login",
        data={"email": "aux3@test.com", "password": "AuxPass123!"},
    )
    aux_token = resp.json()["access_token"]

    resp2 = client.post(
        "/api/v1/auth/registro",
        json={
            "email": "otro3@test.com",
            "full_name": "Otro Tres",
            "role": "auxiliar",
            "password": "Pass1234!",
            "is_active": True,
        },
        headers={"Authorization": f"Bearer {aux_token}"},
    )
    assert resp2.status_code == 403
