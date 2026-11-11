from typing import Any
from app.crud.crud_base import CRUDBase
from app.models.historia_clinica import HistoriaClinica
from app.models.evolucion import Evolucion


historia_clinica = CRUDBase[HistoriaClinica, Any, Any](HistoriaClinica)
evolucion = CRUDBase[Evolucion, Any, Any](Evolucion)
