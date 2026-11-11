from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.dependencies import get_db, get_current_user, require_roles
from app.crud import medico as crud_medico, afiliado as crud_afiliado
from app.models.user import User
from app.models.medico import Medico
from app.schemas import MedicoCreate, MedicoUpdate, MedicoOut, EspecialidadCreate, EspecialidadOut
from app.models.especialidad import Especialidad

router = APIRouter()


@router.post("/", response_model=MedicoOut, status_code=status.HTTP_201_CREATED)
def crear_medico(
    medico_in: MedicoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar")),
):
    if crud_medico.get_by_licencia(db, numero_licencia=medico_in.numero_licencia):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de licencia ya está registrado",
        )
    return crud_medico.create(db, obj_in=medico_in)


@router.get("/", response_model=List[MedicoOut])
def listar_medicos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico", "auxiliar", "auditor")),
):
    return crud_medico.get_multi(db, skip=skip, limit=limit)


@router.get("/{medico_id}", response_model=MedicoOut)
def obtener_medico(
    medico_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico", "auxiliar", "auditor")),
):
    db_medico = crud_medico.get(db, id=medico_id)
    if not db_medico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado")
    return db_medico


@router.put("/{medico_id}", response_model=MedicoOut)
def actualizar_medico(
    medico_id: int,
    medico_in: MedicoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar")),
):
    db_medico = crud_medico.get(db, id=medico_id)
    if not db_medico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado")
    return crud_medico.update(db, db_obj=db_medico, obj_in=medico_in)


@router.post("/especialidades", response_model=EspecialidadOut, status_code=status.HTTP_201_CREATED)
def crear_especialidad(
    esp_in: EspecialidadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    existente = db.execute(
        select(Especialidad).where(Especialidad.nombre == esp_in.nombre)
    ).scalars().first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La especialidad ya existe",
        )
    db_esp = Especialidad(**esp_in.model_dump())
    db.add(db_esp)
    db.commit()
    db.refresh(db_esp)
    return db_esp
