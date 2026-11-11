import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, Button, Input, Alert } from "@/components/ui";
import { useAuth } from "@/context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = new FormData(e.currentTarget as HTMLFormElement);
    const email = form.get("email") as string;
    const password = form.get("password") as string;
    setLoading(true);
    setError("");
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.message || "Credenciales incorrectas");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-eps-50">
      <Card className="w-full max-w-md">
        <h2 className="text-2xl font-bold text-center mb-6 text-eps-700">Iniciar sesión</h2>
        {error && <Alert variant="error">{error}</Alert>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="Correo electrónico" type="email" name="email" required placeholder="admin@eps.com" />
          <Input label="Contraseña" type="password" name="password" required placeholder="••••••••" />
          <Button variant="primary" type="submit" disabled={loading} className="w-full">
            {loading ? "Ingresando..." : "Ingresar"}
          </Button>
        </form>
        <p className="text-center text-sm text-gray-600 mt-4">
          Credenciales de prueba: admin@eps.com / AdminSecure2024!
        </p>
      </Card>
    </div>
  );
}

