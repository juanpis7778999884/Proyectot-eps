from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum


# --- Enums ---
class UserRole(str, Enum):
    admin = "admin"
    medico = "medico"
    auxiliar = "auxiliar"
    auditor = "auditor"
    paciente = "paciente"


class CitaEstado(str, Enum):
    agendada = "agendada"
    completada = "completada"
    cancelada = "cancelada"
    no_asistio = "no_asistio"


class OrdenEstado(str, Enum):
    solicitada = "solicitada"
    autorizada = "autorizada"
    rechazada = "rechazada"
    cumplida = "cumplida"


class FacturaEstado(str, Enum):
    pendiente = "pendiente"
    pagada = "pagada"
    anulada = "anulada"


class OrdenTipo(str, Enum):
    procedimiento = "procedimiento"
    medicamento = "medicamento"
    examen = "examen"


# --- Token ---
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None


class TokenRefresh(BaseModel):
    refresh_token: str


# --- User ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    role: UserRole = UserRole.auxiliar
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

    @validator("password")
    def password_complejidad(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Especialidad ---
class EspecialidadBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None
    activo: bool = True


class EspecialidadCreate(EspecialidadBase):
    pass


class EspecialidadOut(EspecialidadBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Medico ---
class MedicoBase(BaseModel):
    numero_licencia: str = Field(..., min_length=3, max_length=100)
    nombre: str = Field(..., min_length=2, max_length=255)
    especialidad_id: Optional[int] = None
    consultorio: Optional[str] = Field(None, max_length=50)
    telefono: Optional[str] = Field(None, max_length=50)
    activo: bool = True


class MedicoCreate(MedicoBase):
    pass


class MedicoUpdate(BaseModel):
    numero_licencia: Optional[str] = Field(None, min_length=3, max_length=100)
    nombre: Optional[str] = Field(None, min_length=2, max_length=255)
    especialidad_id: Optional[int] = None
    consultorio: Optional[str] = Field(None, max_length=50)
    telefono: Optional[str] = Field(None, max_length=50)
    activo: Optional[bool] = None


class MedicoOut(MedicoBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Afiliado ---
class AfiliadoBase(BaseModel):
    tipo_documento: str = Field(..., min_length=2, max_length=20)
    numero_documento: str = Field(..., min_length=5, max_length=50)
    nombre: str = Field(..., min_length=2, max_length=255)
    apellido: str = Field(..., min_length=2, max_length=255)
    fecha_nacimiento: Optional[datetime] = None
    genero: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=50)
    direccion: Optional[str] = None
    plan: str = Field(..., min_length=2, max_length=100)
    estado: str = Field(..., min_length=2, max_length=50)


class AfiliadoCreate(AfiliadoBase):
    pass


class AfiliadoUpdate(BaseModel):
    tipo_documento: Optional[str] = Field(None, min_length=2, max_length=20)
    numero_documento: Optional[str] = Field(None, min_length=5, max_length=50)
    nombre: Optional[str] = Field(None, min_length=2, max_length=255)
    apellido: Optional[str] = Field(None, min_length=2, max_length=255)
    fecha_nacimiento: Optional[datetime] = None
    genero: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=50)
    direccion: Optional[str] = None
    plan: Optional[str] = Field(None, min_length=2, max_length=100)
    estado: Optional[str] = Field(None, min_length=2, max_length=50)


class AfiliadoOut(AfiliadoBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Cita ---
class CitaBase(BaseModel):
    afiliado_id: int
    medico_id: int
    fecha_hora: datetime
    motivo: Optional[str] = None
    observaciones: Optional[str] = None


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):
    fecha_hora: Optional[datetime] = None
    estado: Optional[CitaEstado] = None
    motivo: Optional[str] = None
    observaciones: Optional[str] = None


class CitaOut(CitaBase):
    id: int
    estado: CitaEstado
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Historia Clinica ---
class HistoriaClinicaOut(BaseModel):
    id: int
    afiliado_id: int
    numero_historia: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Evolucion ---
class EvolucionBase(BaseModel):
    historia_clinica_id: int
    medico_id: int
    fecha: datetime
    motivo_consulta: Optional[str] = None
    examen_fisico: Optional[str] = None
    diagnosticos: Optional[str] = None
    plan_tratamiento: Optional[str] = None
    recetas: Optional[str] = None


class EvolucionCreate(EvolucionBase):
    pass


class EvolucionOut(EvolucionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Medicamento ---
class MedicamentoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=255)
    principio_activo: Optional[str] = Field(None, max_length=255)
    concentracion: Optional[str] = Field(None, max_length=100)
    laboratorio: Optional[str] = Field(None, max_length=255)
    precio_unitario: Optional[float] = Field(None, ge=0)
    stock: int = Field(0, ge=0)
    activo: bool = True


class MedicamentoCreate(MedicamentoBase):
    pass


class MedicamentoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=255)
    principio_activo: Optional[str] = Field(None, max_length=255)
    concentracion: Optional[str] = Field(None, max_length=100)
    laboratorio: Optional[str] = Field(None, max_length=255)
    precio_unitario: Optional[float] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None


class MedicamentoOut(MedicamentoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Orden Medica ---
class OrdenMedicaBase(BaseModel):
    afiliado_id: int
    medico_id: int
    tipo: OrdenTipo
    detalle: str = Field(..., min_length=1, max_length=4000)


class OrdenMedicaCreate(OrdenMedicaBase):
    pass


class OrdenMedicaUpdate(BaseModel):
    tipo: Optional[OrdenTipo] = None
    detalle: Optional[str] = Field(None, min_length=1, max_length=4000)
    estado: Optional[OrdenEstado] = None


class OrdenMedicaOut(OrdenMedicaBase):
    id: int
    numero_orden: str
    estado: OrdenEstado
    fecha: datetime
    autorizado_por: Optional[int] = None
    fecha_autorizacion: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Dispensacion ---
class DispensacionBase(BaseModel):
    orden_id: Optional[int] = None
    medicamento_id: int
    farmaceutico_id: int
    cantidad: int = Field(..., ge=1)
    observaciones: Optional[str] = None


class DispensacionCreate(DispensacionBase):
    pass


class DispensacionOut(DispensacionBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True


# --- Factura ---
class FacturaBase(BaseModel):
    afiliado_id: int
    monto: float = Field(..., ge=0)
    estado: FacturaEstado = FacturaEstado.pendiente
    detalle: Optional[str] = None


class FacturaCreate(FacturaBase):
    pass


class FacturaUpdate(BaseModel):
    monto: Optional[float] = Field(None, ge=0)
    estado: Optional[FacturaEstado] = None
    detalle: Optional[str] = None


class FacturaOut(FacturaBase):
    id: int
    numero_factura: str
    fecha: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# --- Auditoria ---
class AuditoriaOut(BaseModel):
    id: int
    usuario_id: Optional[int] = None
    accion: str
    entidad: str
    entidad_id: Optional[int] = None
    datos_anteriores: Optional[str] = None
    datos_nuevos: Optional[str] = None
    ip: Optional[str] = None
    request_id: Optional[str] = None
    fecha: datetime

    class Config:
        from_attributes = True


# --- Mensaje generico ---
class Mensaje(BaseModel):
    detail: str
