from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user, require_roles
from app.crud import cita as crud_cita, afiliado as crud_afiliado, medico as crud_medico
from app.models.user import User
from app.models.cita import Cita
from app.schemas import CitaCreate, CitaUpdate, CitaOut, Mensaje

router = APIRouter()


@router.post("/", response_model=CitaOut, status_code=status.HTTP_201_CREATED)
def crear_cita(
    cita_in: CitaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar", "medico")),
):
    if not crud_afiliado.get(db, id=cita_in.afiliado_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Afiliado no encontrado")
    if not crud_medico.get(db, id=cita_in.medico_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado")
    existente = crud_cita.get_by_medico_fecha(
        db, medico_id=cita_in.medico_id, fecha_hora=cita_in.fecha_hora
    )
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El médico ya tiene una cita en esa fecha y hora",
        )
    return crud_cita.create(db, obj_in=cita_in)


@router.get("/", response_model=List[CitaOut])
def listar_citas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico", "auxiliar", "auditor")),
):
    return crud_cita.get_multi(db, skip=skip, limit=limit)


@router.get("/{cita_id}", response_model=CitaOut)
def obtener_cita(
    cita_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico", "auxiliar", "auditor")),
):
    db_cita = crud_cita.get(db, id=cita_id)
    if not db_cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    return db_cita


@router.put("/{cita_id}", response_model=CitaOut)
def actualizar_cita(
    cita_id: int,
    cita_in: CitaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar", "medico")),
):
    db_cita = crud_cita.get(db, id=cita_id)
    if not db_cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    if cita_in.fecha_hora is not None and cita_in.medico_id is not None:
        existente = crud_cita.get_by_medico_fecha(
            db, medico_id=cita_in.medico_id, fecha_hora=cita_in.fecha_hora
        )
        if existente and existente.id != cita_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El médico ya tiene una cita en esa fecha y hora",
            )
    return crud_cita.update(db, db_obj=db_cita, obj_in=cita_in)


@router.delete("/{cita_id}", response_model=Mensaje)
def cancelar_cita(
    cita_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar")),
):
    db_cita = crud_cita.remove(db, id=cita_id)
    if not db_cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    return {"detail": "Cita cancelada"}
