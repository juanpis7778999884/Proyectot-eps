from typing import Any
from app.crud.crud_user import user
from app.crud.crud_afiliado import afiliado
from app.crud.crud_medico import medico
from app.crud.crud_cita import cita
from app.crud.crud_historia import historia_clinica, evolucion
from app.crud.crud_orden import orden
from app.crud.crud_farmacia import medicamento, dispensacion
from app.crud.crud_facturacion import factura
from app.crud.crud_auditoria import auditoria

__all__ = [
    "user", "afiliado", "medico", "cita", "historia_clinica", "evolucion",
    "orden", "medicamento", "dispensacion", "factura", "auditoria",
]
