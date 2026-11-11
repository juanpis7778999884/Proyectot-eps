from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.crud.crud_base import CRUDBase
from app.models.cita import Cita
from app.schemas.cita import CitaCreate, CitaUpdate


class CRUDCita(CRUDBase[Cita, CitaCreate, CitaUpdate]):
    def get_by_medico_fecha(
        self, db: Session, *, medico_id: int, fecha_hora
    ) -> Optional[Cita]:
        stmt = select(Cita).where(
            Cita.medico_id == medico_id, Cita.fecha_hora == fecha_hora
        )
        return db.execute(stmt).scalars().first()

    def get_by_afiliado(
        self, db: Session, *, afiliado_id: int, skip: int = 0, limit: int = 100
    ) -> List[Cita]:
        stmt = (
            select(Cita)
            .where(Cita.afiliado_id == afiliado_id)
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())


cita = CRUDCita(Cita)
