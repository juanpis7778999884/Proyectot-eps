from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, Text, UniqueConstraint, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="auxiliar")  # admin, medico, auxiliar, auditor, paciente
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    medico: Mapped[Optional["Medico"]] = relationship(back_populates="user", uselist=False)
    afiliado: Mapped[Optional["Afiliado"]] = relationship(back_populates="user", uselist=False)


class Especialidad(Base):
    __tablename__ = "especialidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    medicos: Mapped[List["Medico"]] = relationship(back_populates="especialidad")


class Medico(Base):
    __tablename__ = "medicos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=True)
    numero_licencia: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    especialidad_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("especialidades.id"), nullable=True)
    consultorio: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    user: Mapped[Optional["User"]] = relationship(back_populates="medico")
    especialidad: Mapped[Optional["Especialidad"]] = relationship(back_populates="medicos")
    citas: Mapped[List["Cita"]] = relationship(back_populates="medico")
    ordenes: Mapped[List["OrdenMedica"]] = relationship(back_populates="medico")
    evoluciones: Mapped[List["Evolucion"]] = relationship(back_populates="medico")


class Afiliado(Base):
    __tablename__ = "afiliados"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=True)
    tipo_documento: Mapped[str] = mapped_column(String(20), nullable=False, default="CC")
    numero_documento: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    apellido: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_nacimiento: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    genero: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    direccion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    plan: Mapped[str] = mapped_column(String(100), nullable=False, default="contributivo")
    estado: Mapped[str] = mapped_column(String(50), nullable=False, default="activo")  # activo, suspendido, retirado
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    user: Mapped[Optional["User"]] = relationship(back_populates="afiliado")
    citas: Mapped[List["Cita"]] = relationship(back_populates="afiliado")
    historias_clinicas: Mapped[List["HistoriaClinica"]] = relationship(back_populates="afiliado")
    ordenes: Mapped[List["OrdenMedica"]] = relationship(back_populates="afiliado")
    facturas: Mapped[List["Factura"]] = relationship(back_populates="afiliado")


class Cita(Base):
    __tablename__ = "citas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    afiliado_id: Mapped[int] = mapped_column(Integer, ForeignKey("afiliados.id"), nullable=False, index=True)
    medico_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicos.id"), nullable=False, index=True)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    estado: Mapped[str] = mapped_column(String(30), nullable=False, default="agendada")  # agendada, completada, cancelada, no_asistio
    motivo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    afiliado: Mapped["Afiliado"] = relationship(back_populates="citas")
    medico: Mapped["Medico"] = relationship(back_populates="citas")


class HistoriaClinica(Base):
    __tablename__ = "historias_clinicas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    afiliado_id: Mapped[int] = mapped_column(Integer, ForeignKey("afiliados.id"), unique=True, nullable=False, index=True)
    numero_historia: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    afiliado: Mapped["Afiliado"] = relationship(back_populates="historias_clinicas")
    evoluciones: Mapped[List["Evolucion"]] = relationship(back_populates="historia_clinica")


class Evolucion(Base):
    __tablename__ = "evoluciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    historia_clinica_id: Mapped[int] = mapped_column(Integer, ForeignKey("historias_clinicas.id"), nullable=False, index=True)
    medico_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicos.id"), nullable=False, index=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    motivo_consulta: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    examen_fisico: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    diagnosticos: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON con códigos CIE-10
    plan_tratamiento: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recetas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON de recetas
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    historia_clinica: Mapped["HistoriaClinica"] = relationship(back_populates="evoluciones")
    medico: Mapped["Medico"] = relationship(back_populates="evoluciones")


class Medicamento(Base):
    __tablename__ = "medicamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    principio_activo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    concentracion: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    laboratorio: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    precio_unitario: Mapped[Optional[float]] = mapped_column(nullable=True)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class OrdenMedica(Base):
    __tablename__ = "ordenes_medicas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    afiliado_id: Mapped[int] = mapped_column(Integer, ForeignKey("afiliados.id"), nullable=False, index=True)
    medico_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicos.id"), nullable=False, index=True)
    numero_orden: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)  # procedimiento, medicamento, examen
    detalle: Mapped[str] = mapped_column(Text, nullable=False)
    estado: Mapped[str] = mapped_column(String(30), nullable=False, default="solicitada")  # solicitada, autorizada, rechazada, cumplida
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    autorizado_por: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    fecha_autorizacion: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    afiliado: Mapped["Afiliado"] = relationship(back_populates="ordenes")
    medico: Mapped["Medico"] = relationship(back_populates="ordenes")


class Dispensacion(Base):
    __tablename__ = "dispensaciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    orden_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("ordenes_medicas.id"), nullable=True, index=True)
    medicamento_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicamentos.id"), nullable=False, index=True)
    farmaceutico_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    medicamento: Mapped["Medicamento"] = relationship()
    farmaceutico: Mapped["User"] = relationship()


class Factura(Base):
    __tablename__ = "facturas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    afiliado_id: Mapped[int] = mapped_column(Integer, ForeignKey("afiliados.id"), nullable=False, index=True)
    numero_factura: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    monto: Mapped[float] = mapped_column(nullable=False)
    estado: Mapped[str] = mapped_column(String(30), nullable=False, default="pendiente")  # pendiente, pagada, anulada
    detalle: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    afiliado: Mapped["Afiliado"] = relationship(back_populates="facturas")


class Auditoria(Base):
    __tablename__ = "auditoria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    usuario_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    accion: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # create, update, delete, login, logout
    entidad: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # usuarios, afiliados, citas, etc.
    entidad_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    datos_anteriores: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    datos_nuevos: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    request_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
