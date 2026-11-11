export interface Usuario {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export interface Afiliado {
  id: number;
  tipo_documento: string;
  numero_documento: string;
  nombre: string;
  apellido: string;
  fecha_nacimiento: string | null;
  genero: string | null;
  email: string | null;
  telefono: string | null;
  direccion: string | null;
  plan: string;
  estado: string;
  user_id: number | null;
  created_at: string;
}

export interface Medico {
  id: number;
  numero_licencia: string;
  nombre: string;
  especialidad_id: number | null;
  consultorio: string | null;
  telefono: string | null;
  activo: boolean;
  user_id: number | null;
  created_at: string;
}

export interface Cita {
  id: number;
  afiliado_id: number;
  medico_id: number;
  fecha_hora: string;
  estado: string;
  motivo: string | null;
  observaciones: string | null;
  created_at: string;
}

export interface Evolucion {
  id: number;
  historia_clinica_id: number;
  medico_id: number;
  fecha: string;
  motivo_consulta: string | null;
  examen_fisico: string | null;
  diagnosticos: string | null;
  plan_tratamiento: string | null;
  recetas: string | null;
  created_at: string;
}

export interface Medicamento {
  id: number;
  nombre: string;
  principio_activo: string | null;
  concentracion: string | null;
  laboratorio: string | null;
  precio_unitario: number | null;
  stock: number;
  activo: boolean;
  created_at: string;
}

export interface OrdenMedica {
  id: number;
  numero_orden: string;
  afiliado_id: number;
  medico_id: number;
  tipo: string;
  detalle: string;
  estado: string;
  fecha: string;
  autorizado_por: number | null;
  fecha_autorizacion: string | null;
  created_at: string;
}

export interface Factura {
  id: number;
  numero_factura: string;
  afiliado_id: number;
  fecha: string;
  monto: number;
  estado: string;
  detalle: string | null;
  created_at: string;
}

export interface Auditoria {
  id: number;
  usuario_id: number | null;
  accion: string;
  entidad: string;
  entidad_id: number | null;
  datos_anteriores: string | null;
  datos_nuevos: string | null;
  ip: string | null;
  request_id: string | null;
  fecha: string;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface AuthUser extends Usuario {
  token: string;
}
