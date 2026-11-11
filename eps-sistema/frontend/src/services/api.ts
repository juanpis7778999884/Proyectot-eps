import { Token } from "@/types";
import type { Usuario, Afiliado, Medico, Cita, Evolucion, Medicamento, OrdenMedica, Factura, Auditoria } from "@/types";

const API_BASE = import.meta.env.VITE_API_URL || "/api";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("eps_token");
}

function setToken(token: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem("eps_token", token);
}

function removeToken() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("eps_token");
}

export { getToken, setToken, removeToken };

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (res.status === 401) {
    removeToken();
    window.location.href = "/login";
    throw new Error("Sesión expirada");
  }

  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(body || `Error ${res.status}`);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  auth: {
    login: (email: string, password: string) =>
      request<Token>("/api/v1/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      }),
    me: () => request<Usuario>("/api/v1/auth/me"),
    registro: (data: any) => request<Usuario>("/api/v1/auth/registro", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  },
  usuarios: {
    list: (skip = 0, limit = 100) =>
      request<Usuario[]>(
        `/api/v1/usuarios/?skip=${skip}&limit=${limit}`
      ),
    get: (id: number) => request<Usuario>(`/api/v1/usuarios/${id}`),
    update: (id: number, data: any) =>
      request<Usuario>(`/api/v1/usuarios/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    remove: (id: number) =>
      request<{ detail: string }>(`/api/v1/usuarios/${id}`, {
        method: "DELETE",
      }),
  },
  afiliados: {
    list: (skip = 0, limit = 100) =>
      request<Afiliado[]>(
        `/api/v1/afiliados/?skip=${skip}&limit=${limit}`
      ),
    get: (id: number) => request<Afiliado>(`/api/v1/afiliados/${id}`),
    create: (data: any) => request<Afiliado>("/api/v1/afiliados/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
    update: (id: number, data: any) =>
      request<Afiliado>(`/api/v1/afiliados/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    remove: (id: number) =>
      request<{ detail: string }>(`/api/v1/afiliados/${id}`, {
        method: "DELETE",
      }),
  },
  medicos: {
    list: (skip = 0, limit = 100) =>
      request<Medico[]>(`/api/v1/medicos/?skip=${skip}&limit=${limit}`),
    get: (id: number) => request<Medico>(`/api/v1/medicos/${id}`),
    create: (data: any) => request<Medico>("/api/v1/medicos/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
    update: (id: number, data: any) =>
      request<Medico>(`/api/v1/medicos/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    especialidad: (data: any) =>
      request<{ nombre: string }>("/api/v1/medicos/especialidades", {
        method: "POST",
        body: JSON.stringify(data),
      }),
  },
  citas: {
    list: (skip = 0, limit = 100) =>
      request<Cita[]>(`/api/v1/citas/?skip=${skip}&limit=${limit}`),
    get: (id: number) => request<Cita>(`/api/v1/citas/${id}`),
    create: (data: any) => request<Cita>("/api/v1/citas/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
    update: (id: number, data: any) =>
      request<Cita>(`/api/v1/citas/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    remove: (id: number) =>
      request<{ detail: string }>(`/api/v1/citas/${id}`, {
        method: "DELETE",
      }),
  },
  historia: {
    getByAfiliado: (id: number) =>
      request<any>(`/api/v1/historia-clinica/${id}`),
    crearEvolucion: (afiliadoId: number, data: any) =>
      request<Evolucion>(
        `/api/v1/historia-clinica/${afiliadoId}/evoluciones`,
        { method: "POST", body: JSON.stringify(data) }
      ),
    listEvoluciones: (afiliadoId: number) =>
      request<Evolucion[]>(
        `/api/v1/historia-clinica/${afiliadoId}/evoluciones`
      ),
  },
  ordenes: {
    list: (skip = 0, limit = 100) =>
      request<OrdenMedica[]>(
        `/api/v1/ordenes/?skip=${skip}&limit=${limit}`
      ),
    get: (id: number) => request<OrdenMedica>(`/api/v1/ordenes/${id}`),
    create: (data: any) => request<OrdenMedica>("/api/v1/ordenes/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
    update: (id: number, data: any) =>
      request<OrdenMedica>(`/api/v1/ordenes/${id}`, {
        method: "PATCH",
        body: JSON.stringify(data),
      }),
  },
  farmacia: {
    listMedicamentos: (skip = 0, limit = 100) =>
      request<Medicamento[]>(
        `/api/v1/farmacia/medicamentos/?skip=${skip}&limit=${limit}`
      ),
    createMedicamento: (data: any) =>
      request<Medicamento>("/api/v1/farmacia/medicamentos/", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    updateMedicamento: (id: number, data: any) =>
      request<Medicamento>(`/api/v1/farmacia/medicamentos/${id}`, {
        method: "PATCH",
        body: JSON.stringify(data),
      }),
    crearDispensacion: (data: any) =>
      request<any>("/api/v1/farmacia/dispensaciones/", {
        method: "POST",
        body: JSON.stringify(data),
      }),
  },
  facturacion: {
    list: (skip = 0, limit = 100) =>
      request<Factura[]>(`/api/v1/facturacion/?skip=${skip}&limit=${limit}`),
    get: (id: number) => request<Factura>(`/api/v1/facturacion/${id}`),
    create: (data: any) => request<Factura>("/api/v1/facturacion/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
    update: (id: number, data: any) =>
      request<Factura>(`/api/v1/facturacion/${id}`, {
        method: "PATCH",
        body: JSON.stringify(data),
      }),
  },
  auditoria: {
    list: (skip = 0, limit = 100, entidad?: string) => {
      const qs = entidad ? `?skip=${skip}&limit=${limit}&entidad=${entidad}` : `?skip=${skip}&limit=${limit}`;
      return request<Auditoria[]>(`/api/v1/auditoria/${qs}`);
    },
  },
};
