import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { AuthProvider } from "@/context/AuthContext";
import { Navbar } from "@/components/Navbar";
import { Outlet } from "react-router-dom";
import Login from "@/pages/Login";
import Dashboard from "@/pages/Dashboard";
import Afiliados from "@/pages/Afiliados";
import Medicos from "@/pages/Medicos";
import Citas from "@/pages/Citas";
import HistoriaClinica from "@/pages/HistoriaClinica";
import Ordenes from "@/pages/Ordenes";
import Farmacia from "@/pages/Farmacia";
import Facturacion from "@/pages/Facturacion";
import Auditoria from "@/pages/Auditoria";

function ProtectedRoute() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Outlet />
      </main>
    </div>
  );
}

const router = createBrowserRouter([
  {
    path: "/login",
    element: React.createElement(Login),
  },
  {
    path: "/",
    element: React.createElement(ProtectedRoute),
    children: [
      { index: true, element: React.createElement(Dashboard) },
      { path: "afiliados", element: React.createElement(Afiliados) },
      { path: "medicos", element: React.createElement(Medicos) },
      { path: "citas", element: React.createElement(Citas) },
      { path: "historia-clinica", element: React.createElement(HistoriaClinica) },
      { path: "ordenes", element: React.createElement(Ordenes) },
      { path: "farmacia", element: React.createElement(Farmacia) },
      { path: "facturacion", element: React.createElement(Facturacion) },
      { path: "auditoria", element: React.createElement(Auditoria) },
    ],
  },
]);

export default function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
}
