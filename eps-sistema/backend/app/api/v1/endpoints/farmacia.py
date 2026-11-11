from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user, require_roles
from app.crud import medicamento as crud_med, dispensacion as crud_disp, orden as crud_orden
from app.models.user import User
from app.models.farmacia import Medicamento, Dispensacion
from app.schemas import MedicamentoCreate, MedicamentoUpdate, MedicamentoOut, DispensacionCreate, DispensacionOut, Mensaje

router = APIRouter()


@router.post("/medicamentos", response_model=MedicamentoOut, status_code=status.HTTP_201_CREATED)
def crear_medicamento(
    med_in: MedicamentoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar")),
):
    return crud_med.create(db, obj_in=med_in)


@router.get("/medicamentos", response_model=List[MedicamentoOut])
def listar_medicamentos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar", "medico", "auditor")),
):
    return crud_med.get_multi(db, skip=skip, limit=limit)


@router.patch("/medicamentos/{med_id}", response_model=MedicamentoOut)
def actualizar_medicamento(
    med_id: int,
    med_in: MedicamentoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar")),
):
    db_med = crud_med.get(db, id=med_id)
    if not db_med:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicamento no encontrado")
    return crud_med.update(db, db_obj=db_med, obj_in=med_in)


@router.post("/dispensaciones", response_model=DispensacionOut, status_code=status.HTTP_201_CREATED)
def crear_dispensacion(
    disp_in: DispensacionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar")),
):
    db_med = crud_med.get(db, id=disp_in.medicamento_id)
    if not db_med:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicamento no encontrado")
    if db_med.stock < disp_in.cantidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock insuficiente",
        )
    db_med.stock -= disp_in.cantidad
    db.add(db_med)
    db_disp = Dispensacion(**disp_in.model_dump())
    db.add(db_disp)
    db.commit()
    db.refresh(db_disp)
    return db_disp
