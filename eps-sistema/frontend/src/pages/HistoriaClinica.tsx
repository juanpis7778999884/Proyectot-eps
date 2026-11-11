import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "react-query";
import { Card, Button, Input, Table, Alert } from "@/components/ui";
import { api } from "@/services/api";

export default function HistoriaClinica() {
  const [afiliadoId, setAfiliadoId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ historia_clinica_id: 1, medico_id: 1, fecha: "", motivo_consulta: "", diagnosticos: "" });

  const { data: hc, isLoading } = useQuery({
    queryKey: ["historia"],
    queryFn: afiliadoId ? () => api.historia.getByAfiliado(afiliadoId) : () => Promise.resolve(null),
    enabled: !!afiliadoId,
  });

  const { data: evoluciones } = useQuery({
    queryKey: ["evoluciones", afiliadoId],
    queryFn: afiliadoId ? () => api.historia.listEvoluciones(afiliadoId) : () => Promise.resolve([]),
    enabled: !!afiliadoId,
  });

  const qc = useQueryClient();
  const evoMut = useMutation({
    mutationFn: (d: any) => api.historia.crearEvolucion(afiliadoId!, d),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["evoluciones", afiliadoId] }); setOpen(false); },
    onError: (err: any) => setError(err.message),
  });

  if (isLoading) return <div className="text-center py-20">Cargando...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-eps-700">Historia Clínica</h2>
        <Input label="ID Afiliado" type="number" value={afiliadoId ?? ""} onChange={e => setAfiliadoId(e.target.value ? Number(e.target.value) : null)} placeholder="Buscar por ID de afiliado" />
      </div>
      {error && <Alert variant="error">{error}</Alert>}
      {afiliadoId && hc && (
        <div className="mb-6">
          <Card>
            <p><strong>Afiliado ID:</strong> {hc.afiliado_id}</p>
            <p><strong>Número de historia:</strong> {hc.numero_historia}</p>
          </Card>
        </div>
      )}
      {afiliadoId && (
        <Table
          columns={[
            { key: "fecha", label: "Fecha" },
            { key: "motivo_consulta", label: "Motivo" },
            { key: "diagnosticos", label: "Diagnósticos" },
          ]}
          data={evoluciones ?? []}
        />
      )}
      {afiliadoId && (
        <div className="mt-6">
          <Button onClick={() => setOpen(true)}>Nueva evolución</Button>
        </div>
      )}
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setOpen(false)} />
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <Card className="w-full max-w-md">
            <h3 className="font-bold text-lg mb-4">Nueva Evolución</h3>
            <form onSubmit={(e) => { e.preventDefault(); evoMut.mutate(form); }} className="space-y-4">
              <Input label="Historia clínica ID" type="number" value={form.historia_clinica_id} onChange={e => setForm({ ...form, historia_clinica_id: Number(e.target.value) })} required />
              <Input label="Médico ID" type="number" value={form.medico_id} onChange={e => setForm({ ...form, medico_id: Number(e.target.value) })} required />
              <Input label="Fecha" type="datetime-local" value={form.fecha} onChange={e => setForm({ ...form, fecha: e.target.value })} required />
              <Input label="Motivo consulta" value={form.motivo_consulta} onChange={e => setForm({ ...form, motivo_consulta: e.target.value })} />
              <Input label="Diagnósticos (CIE-10)" value={form.diagnosticos} onChange={e => setForm({ ...form, diagnosticos: e.target.value })} />
              <div className="flex gap-2">
                <Button variant="ghost" onClick={() => setOpen(false)}>Cancelar</Button>
                <Button type="submit" disabled={evoMut.isLoading}>Guardar</Button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
}

