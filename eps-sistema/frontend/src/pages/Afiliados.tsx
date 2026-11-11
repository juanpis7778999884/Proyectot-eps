import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "react-query";
import { Card, Button, Input, Table, Badge, Alert } from "@/components/ui";
import { api } from "@/services/api";

export default function Afiliados() {
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    tipo_documento: "CC", numero_documento: "", nombre: "", apellido: "",
    genero: "M", email: "", telefono: "", direccion: "", plan: "contributivo", estado: "activo",
  });

  const { data, isLoading } = useQuery({
    queryKey: ["afiliados"],
    queryFn: () => api.afiliados.list(),
  });
  const qc = useQueryClient();

  const createMut = useMutation({
    mutationFn: api.afiliados.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["afiliados"] });
      setOpen(false);
      setError("");
    },
    onError: (err: any) => setError(err.message),
  });

  if (isLoading) return <div className="text-center py-20">Cargando...</div>;

  return (
    <div>
      <div className="flex justify-between items-end mb-6">
        <h2 className="text-2xl font-bold text-eps-700">Afiliados</h2>
        <Button onClick={() => setOpen(true)}>Nuevo afiliado</Button>
      </div>
      {error && <Alert variant="error">{error}</Alert>}
      <Table
        columns={[
          { key: "numero_documento", label: "Documento" },
          { key: "nombre", label: "Nombres" },
          { key: "apellido", label: "Apellidos" },
          { key: "plan", label: "Plan" },
          { key: "estado", label: "Estado", render: (r: any) => <Badge variant={r.estado === "activo" ? "success" : "warning"}>{r.estado}</Badge> },
        ]}
        data={data ?? []}
      />
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setOpen(false)} />
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <Card className="w-full max-w-md">
            <h3 className="font-bold text-lg mb-4">Nuevo Afiliado</h3>
            <form onSubmit={(e) => {
              e.preventDefault();
              createMut.mutate(form);
            }} className="space-y-4">
              <Input label="Tipo documento" value={form.tipo_documento} onChange={e => setForm({ ...form, tipo_documento: e.target.value })} />
              <Input label="Número documento" value={form.numero_documento} onChange={e => setForm({ ...form, numero_documento: e.target.value })} required />
              <Input label="Nombres" value={form.nombre} onChange={e => setForm({ ...form, nombre: e.target.value })} required />
              <Input label="Apellidos" value={form.apellido} onChange={e => setForm({ ...form, apellido: e.target.value })} required />
              <Input label="Género" value={form.genero} onChange={e => setForm({ ...form, genero: e.target.value })} />
              <Input label="Email" type="email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
              <Input label="Teléfono" value={form.telefono} onChange={e => setForm({ ...form, telefono: e.target.value })} />
              <Input label="Plan" value={form.plan} onChange={e => setForm({ ...form, plan: e.target.value })} />
              <Input label="Estado" value={form.estado} onChange={e => setForm({ ...form, estado: e.target.value })} />
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

