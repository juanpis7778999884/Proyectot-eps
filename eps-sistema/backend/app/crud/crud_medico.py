from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.crud.crud_base import CRUDBase
from app.models.medico import Medico
from app.schemas.medico import MedicoCreate, MedicoUpdate


class CRUDMedico(CRUDBase[Medico, MedicoCreate, MedicoUpdate]):
    def get_by_licencia(self, db: Session, *, numero_licencia: str) -> Optional[Medico]:
        stmt = select(Medico).where(Medico.numero_licencia == numero_licencia)
        return db.execute(stmt).scalars().first()


medico = CRUDMedico(Medico)
