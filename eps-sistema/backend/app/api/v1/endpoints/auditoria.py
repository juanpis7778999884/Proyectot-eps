from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user, require_roles
from app.crud import auditoria as crud_auditoria
from app.models.user import User
from app.models.auditoria import Auditoria
from app.schemas import AuditoriaOut, Mensaje

router = APIRouter()


@router.get("/", response_model=List[AuditoriaOut])
def listar_auditoria(
    skip: int = 0,
    limit: int = 100,
    entidad: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auditor")),
):
    from sqlalchemy import select
    stmt = select(Auditoria)
    if entidad:
        stmt = stmt.where(Auditoria.entidad == entidad)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


@router.get("/{auditoria_id}", response_model=AuditoriaOut)
def obtener_auditoria(
    auditoria_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auditor")),
):
    db_aud = crud_auditoria.get(db, id=auditoria_id)
    if not db_aud:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de auditoría no encontrado")
    return db_aud
