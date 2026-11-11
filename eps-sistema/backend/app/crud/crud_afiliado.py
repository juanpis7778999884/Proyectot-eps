from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.crud.crud_base import CRUDBase
from app.models.afiliado import Afiliado
from app.schemas.afiliado import AfiliadoCreate, AfiliadoUpdate


class CRUDAfiliado(CRUDBase[Afiliado, AfiliadoCreate, AfiliadoUpdate]):
    def get_by_documento(self, db: Session, *, numero_documento: str) -> Optional[Afiliado]:
        stmt = select(Afiliado).where(Afiliado.numero_documento == numero_documento)
        return db.execute(stmt).scalars().first()


afiliado = CRUDAfiliado(Afiliado)
