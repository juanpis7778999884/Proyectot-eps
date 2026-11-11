import { useQuery } from "react-query";
import { Card } from "@/components/ui";
import { api } from "@/services/api";

export default function Dashboard() {
  const { data: afiliados, isLoading } = useQuery({
    queryKey: ["afiliados"],
    queryFn: () => api.afiliados.list(0, 5),
  });
  const { data: medicos } = useQuery({
    queryKey: ["medicos"],
    queryFn: () => api.medicos.list(0, 5),
  });
  const { data: citas } = useQuery({
    queryKey: ["citas"],
    queryFn: () => api.citas.list(0, 5),
  });

  if (isLoading) return <div className="text-center py-20">Cargando...</div>;

  return (
    <div className="grid gap-4 md:grid-cols-3">
      <Card>
        <h3 className="font-semibold text-eps-700 mb-2">Afiliados</h3>
        <div className="text-3xl font-bold">{afiliados?.length ?? 0}</div>
      </Card>
      <Card>
        <h3 className="font-semibold text-eps-700 mb-2">Médicos</h3>
        <div className="text-3xl font-bold">{medicos?.length ?? 0}</div>
      </Card>
      <Card>
        <h3 className="font-semibold text-eps-700 mb-2">Citas recientes</h3>
        <div className="text-3xl font-bold">{citas?.length ?? 0}</div>
      </Card>
    </div>
  );
}

