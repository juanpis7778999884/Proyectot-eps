from typing import Any
from app.crud.crud_base import CRUDBase
from app.models.facturacion import Factura
from app.schemas.facturacion import FacturaCreate, FacturaUpdate


factura = CRUDBase[Factura, FacturaCreate, FacturaUpdate](Factura)
