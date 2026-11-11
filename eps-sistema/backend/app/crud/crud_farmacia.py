from typing import Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.crud.crud_base import CRUDBase
from app.models.farmacia import Medicamento, Dispensacion
from app.schemas.farmacia import MedicamentoCreate, MedicamentoUpdate, DispensacionCreate


class CRUDMedicamento(CRUDBase[Medicamento, MedicamentoCreate, MedicamentoUpdate]):
    def get_by_nombre(self, db: Session, *, nombre: str) -> Optional[Medicamento]:
        stmt = select(Medicamento).where(Medicamento.nombre == nombre)
        return db.execute(stmt).scalars().first()


medicamento = CRUDMedicamento(Medicamento)
dispensacion: CRUDBase[Dispensacion, DispensacionCreate, Any] = CRUDBase(
    Dispensacion
)
