from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.crud.crud_base import CRUDBase
from app.models.orden import OrdenMedica
from app.schemas.orden import OrdenMedicaCreate, OrdenMedicaUpdate


class CRUDOrdenMedica(CRUDBase[OrdenMedica, OrdenMedicaCreate, OrdenMedicaUpdate]):
    def get_by_numero(self, db: Session, *, numero_orden: str) -> Optional[OrdenMedica]:
        stmt = select(OrdenMedica).where(OrdenMedica.numero_orden == numero_orden)
        return db.execute(stmt).scalars().first()

    def get_by_afiliado(
        self, db: Session, *, afiliado_id: int, skip: int = 0, limit: int = 100
    ) -> List[OrdenMedica]:
        stmt = (
            select(OrdenMedica)
            .where(OrdenMedica.afiliado_id == afiliado_id)
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())


orden = CRUDOrdenMedica(OrdenMedica)
