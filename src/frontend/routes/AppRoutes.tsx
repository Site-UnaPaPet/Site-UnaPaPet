import { Link, Navigate, Route, Routes } from "react-router-dom";

import { Button } from "@/components/ui/button";
import Formularios from "@/pages/Formularios/Formularios";
import Presenca from "@/pages/Presenca/Presenca";

// Provisório: as outras páginas ainda não existem, então elas mostram este aviso em vez de uma tela em branco.
// Quando uma página ficar pronta, troque o aviso pela página na rota dela.
function EmConstrucao() {
  return (
    <section className="mx-auto flex max-w-md flex-col items-center gap-4 px-4 py-20 text-center">
      <h1 className="font-heading text-3xl text-primary">Página em construção</h1>
      <p className="text-muted-foreground">Esta página ainda não foi criada.</p>
      <Button asChild>
        <Link to="/presenca">Ir para Presença</Link>
      </Button>
    </section>
  );
}

export default function AppRoutes() {
  return (
    <Routes>
      {/* Provisório: a Home ainda não existe, então o início abre a Presença */}
      <Route path="/" element={<Navigate to="/presenca" replace />} />
      <Route path="/presenca" element={<Presenca />} />
      <Route path="/formularios" element={<Formularios />} />
      <Route path="*" element={<EmConstrucao />} />
    </Routes>
  );
}
