import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "react-query";
import { Card, Button, Input, Table, Badge, Alert } from "@/components/ui";
import { api } from "@/services/api";

export default function Ordenes() {
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ afiliado_id: 1, medico_id: 1, tipo: "procedimiento", detalle: "" });

  const { data, isLoading } = useQuery({
    queryKey: ["ordenes"],
    queryFn: () => api.ordenes.list(),
  });
  const qc = useQueryClient();

  const createMut = useMutation({
    mutationFn: api.ordenes.create,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["ordenes"] }); setOpen(false); },
    onError: (err: any) => setError(err.message),
  });

  const authMut = useMutation({
    mutationFn: (id: number) => api.ordenes.update(id, { estado: "autorizada" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["ordenes"] }),
  });

  if (isLoading) return <div className="text-center py-20">Cargando...</div>;

  return (
    <div>
      <div className="flex justify-between items-end mb-6">
        <h2 className="text-2xl font-bold text-eps-700">Órdenes Médicas</h2>
        <Button onClick={() => setOpen(true)}>Nueva orden</Button>
      </div>
      {error && <Alert variant="error">{error}</Alert>}
      <Table
        columns={[
          { key: "numero_orden", label: "Número orden" },
          { key: "tipo", label: "Tipo" },
          { key: "estado", label: "Estado", render: (r: any) => <Badge variant={r.estado === "autorizada" ? "success" : "warning"}>{r.estado}</Badge> },
          { key: "detalle", label: "Detalle" },
          { key: "id", label: "Acciones", render: (r: any) => r.estado !== "autorizada" ? (
            <Button variant="primary" size="sm" onClick={() => authMut.mutate(r.id)}>Autorizar</Button>
          ) : <Badge variant="success">Autorizada</Badge>},
        ]}
        data={data ?? []}
      />
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setOpen(false)} />
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <Card className="w-full max-w-md">
            <h3 className="font-bold text-lg mb-4">Nueva Orden Médica</h3>
            <form onSubmit={(e) => { e.preventDefault(); createMut.mutate(form); }} className="space-y-4">
              <Input label="ID Afiliado" type="number" value={form.afiliado_id} onChange={e => setForm({ ...form, afiliado_id: Number(e.target.value) })} required />
              <Input label="ID Médico" type="number" value={form.medico_id} onChange={e => setForm({ ...form, medico_id: Number(e.target.value) })} required />
              <Input label="Tipo" value={form.tipo} onChange={e => setForm({ ...form, tipo: e.target.value })} required />
              <Input label="Detalle" value={form.detalle} onChange={e => setForm({ ...form, detalle: e.target.value })} required />
              <div className="flex gap-2">
                <Button variant="ghost" onClick={() => setOpen(false)}>Cancelar</Button>
                <Button type="submit" disabled={createMut.isLoading}>Crear</Button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
}

