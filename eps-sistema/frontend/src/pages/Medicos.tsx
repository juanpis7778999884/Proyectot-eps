import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "react-query";
import { Card, Button, Input, Table, Badge, Alert } from "@/components/ui";
import { api } from "@/services/api";

export default function Medicos() {
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ numero_licencia: "", nombre: "", consultorio: "", telefono: "", activo: true });

  const { data, isLoading } = useQuery({
    queryKey: ["medicos"],
    queryFn: () => api.medicos.list(),
  });
  const qc = useQueryClient();

  const createMut = useMutation({
    mutationFn: api.medicos.create,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["medicos"] }); setOpen(false); },
    onError: (err: any) => setError(err.message),
  });

  if (isLoading) return <div className="text-center py-20">Cargando...</div>;

  return (
    <div>
      <div className="flex justify-between items-end mb-6">
        <h2 className="text-2xl font-bold text-eps-700">Médicos</h2>
        <Button onClick={() => setOpen(true)}>Nuevo médico</Button>
      </div>
      {error && <Alert variant="error">{error}</Alert>}
      <Table
        columns={[
          { key: "numero_licencia", label: "Licencia" },
          { key: "nombre", label: "Nombre" },
          { key: "consultorio", label: "Consultorio" },
          { key: "activo", label: "Activo", render: (r: any) => <Badge variant={r.activo ? "success" : "danger"}>{r.activo ? "Sí" : "No"}</Badge> },
        ]}
        data={data ?? []}
      />
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setOpen(false)} />
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <Card className="w-full max-w-md">
            <h3 className="font-bold text-lg mb-4">Nuevo Médico</h3>
            <form onSubmit={(e) => { e.preventDefault(); createMut.mutate(form); }} className="space-y-4">
              <Input label="Número licencia" value={form.numero_licencia} onChange={e => setForm({ ...form, numero_licencia: e.target.value })} required />
              <Input label="Nombre" value={form.nombre} onChange={e => setForm({ ...form, nombre: e.target.value })} required />
              <Input label="Consultorio" value={form.consultorio} onChange={e => setForm({ ...form, consultorio: e.target.value })} />
              <Input label="Teléfono" value={form.telefono} onChange={e => setForm({ ...form, telefono: e.target.value })} />
              <Input label="Activo (true/false)" type="checkbox" checked={form.activo} onChange={e => setForm({ ...form, activo: e.target.checked })} />
              <div className="flex gap-2">
                <Button variant="ghost" onClick={() => setOpen(false)}>Cancelar</Button>
                <Button type="submit" disabled={createMut.isLoading}>Guardar</Button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
}

