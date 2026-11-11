import { useQuery } from "react-query";
import { Table, Alert } from "@/components/ui";
import { api } from "@/services/api";

export default function Auditoria() {
  const { data, isLoading } = useQuery({
    queryKey: ["auditoria"],
    queryFn: () => api.auditoria.list(0, 50),
  });

  if (isLoading) return <div className="text-center py-20">Cargando...</div>;

  return (
    <div>
      <h2 className="text-2xl font-bold text-eps-700 mb-6">Auditoría del Sistema</h2>
      <Table
        columns={[
          { key: "fecha", label: "Fecha" },
          { key: "usuario_id", label: "Usuario ID" },
          { key: "accion", label: "Acción" },
          { key: "entidad", label: "Entidad" },
          { key: "entidad_id", label: "Entidad ID" },
          { key: "ip", label: "IP" },
        ]}
        data={data ?? []}
      />
      {(!data || data.length === 0) && <Alert variant="info">No hay registros de auditoría.</Alert>}
    </div>
  );
}

