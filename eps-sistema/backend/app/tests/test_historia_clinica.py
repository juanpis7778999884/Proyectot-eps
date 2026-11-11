from fastapi.testclient import TestClient
from sqlalchemy import select


def test_crear_evolucion(client: TestClient, auth_headers, afiliado_principal, medico_principal, db):
    from app.models.historia_clinica import HistoriaClinica
    hc = HistoriaClinica(afiliado_id=afiliado_principal.id, numero_historia="HIST000001")
    db.add(hc)
    db.commit()
    db.refresh(hc)

    resp = client.post(
        f"/api/v1/historia-clinica/{afiliado_principal.id}/evoluciones",
        json={
            "historia_clinica_id": hc.id,
            "medico_id": medico_principal.id,
            "fecha": "2026-12-01T10:30:00",
            "motivo_consulta": "Dolor de cabeza",
            "diagnosticos": "CIE-10: R51",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text


def test_listar_evoluciones(client: TestClient, auth_headers, afiliado_principal, db):
    from app.models.historia_clinica import HistoriaClinica
    hc = db.execute(
        select(HistoriaClinica).where(HistoriaClinica.afiliado_id == afiliado_principal.id)
    ).scalars().first()
    if hc is None:
        hc = HistoriaClinica(afiliado_id=afiliado_principal.id, numero_historia="HIST000002")
        db.add(hc)
        db.commit()
        db.refresh(hc)
    resp = client.get(
        f"/api/v1/historia-clinica/{afiliado_principal.id}/evoluciones", headers=auth_headers
    )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_historia_clinica_sin_crear(client: TestClient, auth_headers):
    resp = client.get("/api/v1/historia-clinica/999", headers=auth_headers)
    assert resp.status_code == 404
