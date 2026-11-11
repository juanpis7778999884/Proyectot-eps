import { NavLink } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";

export function Navbar() {
  const { user, logout } = useAuth();
  return (
    <nav className="bg-eps-700 text-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center gap-2">
            <span className="font-bold text-xl tracking-tighter">EPS</span>
            <span className="text-sm opacity-90">Sistema de Gestión</span>
          </div>
          <div className="flex items-center gap-4">
            <NavLink to="/dashboard" className={(props: any) => props.isActive ? "text-eps-300 font-semibold" : "text-eps-200 hover:text-white"}>
              Inicio
            </NavLink>
            <NavLink to="/afiliados" className={(props: any) => props.isActive ? "text-eps-300 font-semibold" : "text-eps-200 hover:text-white"}>
              Afiliados
            </NavLink>
            <NavLink to="/medicos" className={(props: any) => props.isActive ? "text-eps-300 font-semibold" : "text-eps-200 hover:text-white"}>
              Médicos
            </NavLink>
            <NavLink to="/citas" className={(props: any) => props.isActive ? "text-eps-300 font-semibold" : "text-eps-200 hover:text-white"}>
              Citas
            </NavLink>
            <NavLink to="/ordenes" className={(props: any) => props.isActive ? "text-eps-300 font-semibold" : "text-eps-200 hover:text-white"}>
              Órdenes
            </NavLink>
            <NavLink to="/farmacia" className={(props: any) => props.isActive ? "text-eps-300 font-semibold" : "text-eps-200 hover:text-white"}>
              Farmacia
            </NavLink>
            <NavLink to="/facturacion" className={(props: any) => props.isActive ? "text-eps-300 font-semibold" : "text-eps-200 hover:text-white"}>
              Facturación
            </NavLink>
            <NavLink to="/auditoria" className={(props: any) => props.isActive ? "text-eps-300 font-semibold" : "text-eps-200 hover:text-white"}>
              Auditoría
            </NavLink>
            <span className="text-xs opacity-75">{user?.full_name} ({user?.role})</span>
            <button onClick={logout} className="bg-red-600 hover:bg-red-700 text-white px-3 py-1.5 rounded text-sm">Salir</button>
          </div>
        </div>
      </div>
    </nav>
  );
}
