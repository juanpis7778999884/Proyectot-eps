import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "react-query";
import { Card, Button, Input, Table, Badge, Alert } from "@/components/ui";
import { api } from "@/services/api";

export default function Farmacia() {
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ nombre: "", principio_activo: "", concentracion: "", laboratorio: "", precio_unitario: 0, stock: 0, activo: true });
  const [dispForm, setDispForm] = useState({ medicamento_id: 1, farmaceutico_id: 1, cantidad: 1 });

  const { data, isLoading } = useQuery({
    queryKey: ["medicamentos"],
    queryFn: () => api.farmacia.listMedicamentos(),
  });
  const qc = useQueryClient();

  const medMut = useMutation({
    mutationFn: api.farmacia.createMedicamento,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["medicamentos"] }); setOpen(false); },
    onError: (err: any) => setError(err.message),
  });

  const dispMut = useMutation({
    mutationFn: api.farmacia.crearDispensacion,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["medicamentos"] }),
    onError: (err: any) => setError(err.message),
  });

  if (isLoading) return <div className="text-center py-20">Cargando...</div>;

  return (
    <div>
      <div className="flex justify-between items-end mb-6">
        <h2 className="text-2xl font-bold text-eps-700">Farmacia</h2>
        <Button onClick={() => setOpen(true)}>Nuevo medicamento</Button>
      </div>
      {error && <Alert variant="error">{error}</Alert>}
      <Table
        columns={[
          { key: "nombre", label: "Medicamento" },
          { key: "concentracion", label: "Concentración" },
          { key: "stock", label: "Stock" },
          { key: "activo", label: "Activo", render: (r: any) => <Badge variant={r.activo ? "success" : "danger"}>{r.activo ? "Sí" : "No"}</Badge> },
        ]}
        data={data ?? []}
      />
      <div className="mt-8">
        <h3 className="font-bold text-lg mb-3 text-eps-700">Dispensar medicamento</h3>
        <form onSubmit={(e) => { e.preventDefault(); dispMut.mutate(dispForm); }} className="space-y-4 max-w-sm">
          <Input label="ID Medicamento" type="number" value={dispForm.medicamento_id} onChange={e => setDispForm({ ...dispForm, medicamento_id: Number(e.target.value) })} required />
          <Input label="ID Farmacéutico" type="number" value={dispForm.farmaceutico_id} onChange={e => setDispForm({ ...dispForm, farmaceutico_id: Number(e.target.value) })} required />
          <Input label="Cantidad" type="number" value={dispForm.cantidad} onChange={e => setDispForm({ ...dispForm, cantidad: Number(e.target.value) })} required />
          <Button type="submit" disabled={dispMut.isLoading}>Dispensar</Button>
        </form>
      </div>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setOpen(false)} />
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <Card className="w-full max-w-md">
            <h3 className="font-bold text-lg mb-4">Nuevo Medicamento</h3>
            <form onSubmit={(e) => { e.preventDefault(); medMut.mutate(form); }} className="space-y-4">
              <Input label="Nombre" value={form.nombre} onChange={e => setForm({ ...form, nombre: e.target.value })} required />
              <Input label="Principio activo" value={form.principio_activo} onChange={e => setForm({ ...form, principio_activo: e.target.value })} />
              <Input label="Concentración" value={form.concentracion} onChange={e => setForm({ ...form, concentracion: e.target.value })} />
              <Input label="Laboratorio" value={form.laboratorio} onChange={e => setForm({ ...form, laboratorio: e.target.value })} />
              <Input label="Precio unitario" type="number" value={form.precio_unitario} onChange={e => setForm({ ...form, precio_unitario: Number(e.target.value) })} />
              <Input label="Stock" type="number" value={form.stock} onChange={e => setForm({ ...form, stock: Number(e.target.value) })} />
              <Input label="Activo (true/false)" type="checkbox" checked={form.activo} onChange={e => setForm({ ...form, activo: e.target.checked })} />
              <div className="flex gap-2">
                <Button variant="ghost" onClick={() => setOpen(false)}>Cancelar</Button>
                <Button type="submit" disabled={medMut.isLoading}>Guardar</Button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
}

