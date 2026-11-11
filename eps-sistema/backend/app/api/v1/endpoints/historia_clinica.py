from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.dependencies import get_db, get_current_user, require_roles
from app.crud import historia_clinica as crud_hc, evolucion as crud_evo, afiliado as crud_afiliado, medico as crud_medico
from app.models.user import User
from app.models.historia_clinica import HistoriaClinica
from app.models.evolucion import Evolucion
from app.schemas import HistoriaClinicaOut, EvolucionCreate, EvolucionOut, Mensaje

router = APIRouter()


@router.get("/{afiliado_id}", response_model=HistoriaClinicaOut)
def obtener_historia(
    afiliado_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico", "auxiliar", "auditor")),
):
    hc = db.execute(
        select(HistoriaClinica).where(HistoriaClinica.afiliado_id == afiliado_id)
    ).scalars().first()
    if not hc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Historia clínica no encontrada")
    return hc


@router.post("/{afiliado_id}/evoluciones", response_model=EvolucionOut, status_code=status.HTTP_201_CREATED)
def crear_evolucion(
    afiliado_id: int,
    evo_in: EvolucionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico")),
):
    if evo_in.historia_clinica_id:
        hc = db.get(HistoriaClinica, evo_in.historia_clinica_id)
        if not hc or hc.afiliado_id != afiliado_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Historia clínica no pertenece a este afiliado")
    if not crud_medico.get(db, id=evo_in.medico_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado")
    return crud_evo.create(db, obj_in=evo_in)


@router.get("/{afiliado_id}/evoluciones", response_model=List[EvolucionOut])
def listar_evoluciones(
    afiliado_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico", "auxiliar", "auditor")),
):
    hc = db.execute(
        select(HistoriaClinica).where(HistoriaClinica.afiliado_id == afiliado_id)
    ).scalars().first()
    if not hc:
        return []
    return crud_evo.get_multi(db).filter(Evolucion.historia_clinica_id == hc.id).all() if False else list(
        db.execute(
            select(Evolucion).where(Evolucion.historia_clinica_id == hc.id)
        ).scalars().all()
    )
