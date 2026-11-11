from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user, require_roles
from app.crud import orden as crud_orden, afiliado as crud_afiliado, medico as crud_medico
from app.models.user import User
from app.models.orden import OrdenMedica
from app.schemas import OrdenMedicaCreate, OrdenMedicaUpdate, OrdenMedicaOut, Mensaje

router = APIRouter()


from datetime import datetime, timezone


@router.post("/", response_model=OrdenMedicaOut, status_code=status.HTTP_201_CREATED)
def crear_orden(
    orden_in: OrdenMedicaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico")),
):
    if not crud_afiliado.get(db, id=orden_in.afiliado_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Afiliado no encontrado")
    if not crud_medico.get(db, id=orden_in.medico_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado")
    numero = f"ORD-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{orden_in.afiliado_id}"
    db_orden = OrdenMedica(**orden_in.model_dump(), numero_orden=numero)
    db.add(db_orden)
    db.commit()
    db.refresh(db_orden)
    return db_orden


@router.get("/", response_model=List[OrdenMedicaOut])
def listar_ordenes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico", "auxiliar", "auditor")),
):
    return crud_orden.get_multi(db, skip=skip, limit=limit)


@router.get("/{orden_id}", response_model=OrdenMedicaOut)
def obtener_orden(
    orden_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico", "auxiliar", "auditor")),
):
    db_orden = crud_orden.get(db, id=orden_id)
    if not db_orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return db_orden


@router.patch("/{orden_id}", response_model=OrdenMedicaOut)
def actualizar_orden(
    orden_id: int,
    orden_in: OrdenMedicaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico")),
):
    db_orden = crud_orden.get(db, id=orden_id)
    if not db_orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    update_data = orden_in.model_dump(exclude_unset=True)
    if "estado" in update_data and update_data["estado"] == "autorizada":
        update_data["autorizado_por"] = current_user.id
        from datetime import datetime, timezone
        update_data["fecha_autorizacion"] = datetime.now(timezone.utc)
    return crud_orden.update(db, db_obj=db_orden, obj_in=update_data)
