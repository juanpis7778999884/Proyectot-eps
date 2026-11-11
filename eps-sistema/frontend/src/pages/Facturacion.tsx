import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "react-query";
import { Card, Button, Input, Table, Badge, Alert } from "@/components/ui";
import { api } from "@/services/api";

export default function Facturacion() {
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ afiliado_id: 1, monto: 0, estado: "pendiente", detalle: "" });

  const { data, isLoading } = useQuery({
    queryKey: ["facturas"],
    queryFn: () => api.facturacion.list(),
  });
  const qc = useQueryClient();

  const createMut = useMutation({
    mutationFn: api.facturacion.create,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["facturas"] }); setOpen(false); },
    onError: (err: any) => setError(err.message),
  });

  const payMut = useMutation({
    mutationFn: (id: number) => api.facturacion.update(id, { estado: "pagada" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["facturas"] }),
  });

  if (isLoading) return <div className="text-center py-20">Cargando...</div>;

  return (
    <div>
      <div className="flex justify-between items-end mb-6">
        <h2 className="text-2xl font-bold text-eps-700">Facturación</h2>
        <Button onClick={() => setOpen(true)}>Nueva factura</Button>
      </div>
      {error && <Alert variant="error">{error}</Alert>}
      <Table
        columns={[
          { key: "numero_factura", label: "Factura" },
          { key: "monto", label: "Monto", render: (r: any) => `$${r.monto}` },
          { key: "estado", label: "Estado", render: (r: any) => <Badge variant={r.estado === "pagada" ? "success" : "warning"}>{r.estado}</Badge> },
          { key: "id", label: "Acciones", render: (r: any) => r.estado !== "pagada" ? (
            <Button variant="primary" size="sm" onClick={() => payMut.mutate(r.id)}>Marcar pagada</Button>
          ) : <Badge variant="success">Pagada</Badge>},
        ]}
        data={data ?? []}
      />
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setOpen(false)} />
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <Card className="w-full max-w-md">
            <h3 className="font-bold text-lg mb-4">Nueva Factura</h3>
            <form onSubmit={(e) => { e.preventDefault(); createMut.mutate(form); }} className="space-y-4">
              <Input label="ID Afiliado" type="number" value={form.afiliado_id} onChange={e => setForm({ ...form, afiliado_id: Number(e.target.value) })} required />
              <Input label="Monto" type="number" value={form.monto} onChange={e => setForm({ ...form, monto: Number(e.target.value) })} required />
              <Input label="Estado" value={form.estado} onChange={e => setForm({ ...form, estado: e.target.value })} required />
              <Input label="Detalle" value={form.detalle} onChange={e => setForm({ ...form, detalle: e.target.value })} />
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

