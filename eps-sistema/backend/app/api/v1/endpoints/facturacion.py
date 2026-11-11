from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user, require_roles
from app.crud import factura as crud_factura, afiliado as crud_afiliado
from app.models.user import User
from app.models.facturacion import Factura
from app.schemas import FacturaCreate, FacturaUpdate, FacturaOut, Mensaje

router = APIRouter()


from datetime import datetime, timezone


@router.post("/", response_model=FacturaOut, status_code=status.HTTP_201_CREATED)
def crear_factura(
    factura_in: FacturaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar")),
):
    if not crud_afiliado.get(db, id=factura_in.afiliado_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Afiliado no encontrado")
    numero = f"FAC-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{factura_in.afiliado_id}"
    db_factura = Factura(**factura_in.model_dump(), numero_factura=numero)
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura


@router.get("/", response_model=List[FacturaOut])
def listar_facturas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar", "auditor")),
):
    return crud_factura.get_multi(db, skip=skip, limit=limit)


@router.get("/{factura_id}", response_model=FacturaOut)
def obtener_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar", "auditor")),
):
    db_factura = crud_factura.get(db, id=factura_id)
    if not db_factura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
    return db_factura


@router.patch("/{factura_id}", response_model=FacturaOut)
def actualizar_factura(
    factura_id: int,
    factura_in: FacturaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar")),
):
    db_factura = crud_factura.get(db, id=factura_id)
    if not db_factura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
    return crud_factura.update(db, db_obj=db_factura, obj_in=factura_in)
