import os
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect

os.environ["TESTING"] = "true"

from app.main import app
from app.db.base import Base
from app.db.session import engine, SessionLocal

TEST_DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "test_eps.db"
)


@pytest.fixture(scope="session", autouse=True)
def inicializar_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    Base.metadata.create_all(bind=engine)
    tablas = inspect(engine).get_table_names()
    assert "users" in tablas, f"Tabla users no creada. Tablas: {tablas}"
    yield
    try:
        engine.dispose()
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
    except Exception:
        pass


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    yield db
    db.rollback()
    db.close()


@pytest.fixture(scope="module")
def superuser(client):
    db = SessionLocal()
    try:
        from app.crud import user as crud_user
        from app.schemas import UserCreate

        existing = crud_user.get_by_email(db, email="admin@test.com")
        if not existing:
            db_user = crud_user.create(
                db,
                obj_in=UserCreate(
                    email="admin@test.com",
                    full_name="Admin Test",
                    role="admin",
                    password="AdminSecure2024!",
                    is_active=True,
                ),
            )
            db.commit()
            db.refresh(db_user)
        else:
            db_user = existing
        return db_user
    finally:
        db.close()


@pytest.fixture(scope="function")
def afiliado_principal(client, superuser, db):
    from app.crud import afiliado as crud_afiliado
    from app.schemas import AfiliadoCreate
    suf = uuid.uuid4().hex[:8]
    a = crud_afiliado.create(db, obj_in=AfiliadoCreate(
        tipo_documento="CC", numero_documento=f"1000000{suf}",
        nombre="Paciente", apellido="Prueba", plan="contributivo", estado="activo",
    ))
    db.commit()
    db.refresh(a)
    return a


@pytest.fixture(scope="function")
def medico_principal(client, superuser, db):
    from app.crud import medico as crud_medico
    from app.schemas import MedicoCreate
    suf = uuid.uuid4().hex[:8]
    m = crud_medico.create(db, obj_in=MedicoCreate(
        numero_licencia=f"MED{suf}", nombre="Médico Prueba", activo=True,
    ))
    db.commit()
    db.refresh(m)
    return m


@pytest.fixture(scope="module")
def superuser_token(client, superuser):
    resp = client.post(
        "/api/v1/auth/login",
        data={"email": "admin@test.com", "password": "AdminSecure2024!"},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


@pytest.fixture(scope="module")
def auth_headers(superuser_token):
    return {"Authorization": f"Bearer {superuser_token}"}
