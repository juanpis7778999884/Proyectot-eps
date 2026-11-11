from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user, require_roles
from app.crud import afiliado as crud_afiliado
from app.models.user import User
from app.models.afiliado import Afiliado
from app.schemas import AfiliadoCreate, AfiliadoUpdate, AfiliadoOut, Mensaje

router = APIRouter()


@router.post("/", response_model=AfiliadoOut, status_code=status.HTTP_201_CREATED)
def crear_afiliado(
    afiliado_in: AfiliadoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar")),
):
    if crud_afiliado.get_by_documento(db, numero_documento=afiliado_in.numero_documento):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de documento ya está registrado",
        )
    return crud_afiliado.create(db, obj_in=afiliado_in)


@router.get("/", response_model=List[AfiliadoOut])
def listar_afiliados(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico", "auxiliar", "auditor")),
):
    return crud_afiliado.get_multi(db, skip=skip, limit=limit)


@router.get("/{afiliado_id}", response_model=AfiliadoOut)
def obtener_afiliado(
    afiliado_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "medico", "auxiliar", "auditor", "paciente")),
):
    db_afiliado = crud_afiliado.get(db, id=afiliado_id)
    if not db_afiliado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Afiliado no encontrado")
    return db_afiliado


@router.put("/{afiliado_id}", response_model=AfiliadoOut)
def actualizar_afiliado(
    afiliado_id: int,
    afiliado_in: AfiliadoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "auxiliar")),
):
    db_afiliado = crud_afiliado.get(db, id=afiliado_id)
    if not db_afiliado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Afiliado no encontrado")
    return crud_afiliado.update(db, db_obj=db_afiliado, obj_in=afiliado_in)


@router.delete("/{afiliado_id}", response_model=Mensaje)
def eliminar_afiliado(
    afiliado_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    db_afiliado = crud_afiliado.remove(db, id=afiliado_id)
    if not db_afiliado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Afiliado no encontrado")
    return {"detail": "Afiliado eliminado"}
