import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "react-query";
import { Card, Button, Input, Table, Badge, Alert } from "@/components/ui";
import { api } from "@/services/api";

export default function Citas() {
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ afiliado_id: 1, medico_id: 1, fecha_hora: "", motivo: "" });

  const { data, isLoading } = useQuery({
    queryKey: ["citas"],
    queryFn: () => api.citas.list(),
  });
  const qc = useQueryClient();

  const createMut = useMutation({
    mutationFn: api.citas.create,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["citas"] }); setOpen(false); },
    onError: (err: any) => setError(err.message),
  });

  const removeMut = useMutation({
    mutationFn: api.citas.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["citas"] }),
  });

  if (isLoading) return <div className="text-center py-20">Cargando...</div>;

  return (
    <div>
      <div className="flex justify-between items-end mb-6">
        <h2 className="text-2xl font-bold text-eps-700">Citas Médicas</h2>
        <Button onClick={() => setOpen(true)}>Agendar cita</Button>
      </div>
      {error && <Alert variant="error">{error}</Alert>}
      <Table
        columns={[
          { key: "fecha_hora", label: "Fecha y hora" },
          { key: "estado", label: "Estado", render: (r: any) => <Badge variant={r.estado === "agendada" ? "success" : "warning"}>{r.estado}</Badge> },
          { key: "motivo", label: "Motivo" },
          { key: "id", label: "Acciones", render: (r: any) => (
            <Button variant="danger" size="sm" onClick={() => removeMut.mutate(r.id)}>Cancelar</Button>
          )},
        ]}
        data={data ?? []}
      />
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setOpen(false)} />
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <Card className="w-full max-w-md">
            <h3 className="font-bold text-lg mb-4">Agendar Cita</h3>
            <form onSubmit={(e) => { e.preventDefault(); createMut.mutate(form); }} className="space-y-4">
              <Input label="ID Afiliado" type="number" value={form.afiliado_id} onChange={e => setForm({ ...form, afiliado_id: Number(e.target.value) })} required />
              <Input label="ID Médico" type="number" value={form.medico_id} onChange={e => setForm({ ...form, medico_id: Number(e.target.value) })} required />
              <Input label="Fecha y hora" type="datetime-local" value={form.fecha_hora} onChange={e => setForm({ ...form, fecha_hora: e.target.value })} required />
              <Input label="Motivo" value={form.motivo} onChange={e => setForm({ ...form, motivo: e.target.value })} />
              <div className="flex gap-2">
                <Button variant="ghost" onClick={() => setOpen(false)}>Cancelar</Button>
                <Button type="submit" disabled={createMut.isLoading}>Agendar</Button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
}

