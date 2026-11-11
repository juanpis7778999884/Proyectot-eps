from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.middleware import SecurityHeadersMiddleware, AuditMiddleware, RateLimitMiddleware
from app.db.session import SessionLocal
from app.api.v1.endpoints import auth, users, afiliados, medicos, citas, historia_clinica, ordenes, farmacia, facturacion, auditoria

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuditMiddleware)
app.add_middleware(RateLimitMiddleware, calls=settings.RATE_LIMIT_PER_MINUTE, period=60)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)


@app.get("/health")
def health():
    return {"status": "healthy", "service": settings.PROJECT_NAME}


app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/usuarios", tags=["usuarios"])
app.include_router(afiliados.router, prefix=f"{settings.API_V1_STR}/afiliados", tags=["afiliados"])
app.include_router(medicos.router, prefix=f"{settings.API_V1_STR}/medicos", tags=["medicos"])
app.include_router(citas.router, prefix=f"{settings.API_V1_STR}/citas", tags=["citas"])
app.include_router(historia_clinica.router, prefix=f"{settings.API_V1_STR}/historia-clinica", tags=["historia-clinica"])
app.include_router(ordenes.router, prefix=f"{settings.API_V1_STR}/ordenes", tags=["ordenes"])
app.include_router(farmacia.router, prefix=f"{settings.API_V1_STR}/farmacia", tags=["farmacia"])
app.include_router(facturacion.router, prefix=f"{settings.API_V1_STR}/facturacion", tags=["facturacion"])
app.include_router(auditoria.router, prefix=f"{settings.API_V1_STR}/auditoria", tags=["auditoria"])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor", "type": "server_error"},
    )
