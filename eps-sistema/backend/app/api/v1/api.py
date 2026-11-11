from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, users, afiliados, medicos, citas, historia_clinica,
    ordenes, farmacia, facturacion, auditoria,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/usuarios", tags=["usuarios"])
api_router.include_router(afiliados.router, prefix="/afiliados", tags=["afiliados"])
api_router.include_router(medicos.router, prefix="/medicos", tags=["medicos"])
api_router.include_router(citas.router, prefix="/citas", tags=["citas"])
api_router.include_router(
    historia_clinica.router, prefix="/historia-clinica", tags=["historia-clinica"]
)
api_router.include_router(ordenes.router, prefix="/ordenes", tags=["ordenes"])
api_router.include_router(farmacia.router, prefix="/farmacia", tags=["farmacia"])
api_router.include_router(facturacion.router, prefix="/facturacion", tags=["facturacion"])
api_router.include_router(auditoria.router, prefix="/auditoria", tags=["auditoria"])
