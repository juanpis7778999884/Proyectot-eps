from typing import Any
from app.crud.crud_base import CRUDBase
from app.models.auditoria import Auditoria


auditoria = CRUDBase[Auditoria, Any, Any](Auditoria)
