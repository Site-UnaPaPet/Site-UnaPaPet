import { useEffect, useState } from "react";
import { ArrowRight, ClipboardList, FileText } from "lucide-react";

import filhotes from "@/assets/filhotes-formularios.webp";
import PageBanner from "@/components/layout/PageBanner";
import { Button } from "@/components/ui/button";
import { ApiError } from "@/services/api";
import { listarFormularios, type Formulario } from "@/services/formularios";

export default function Formularios() {
  const [formularios, setFormularios] = useState<Formulario[] | null>(null); // null = carregando
  const [erro, setErro] = useState("");

  useEffect(() => {
    listarFormularios()
      .then(setFormularios)
      .catch((e: unknown) => setErro(e instanceof ApiError ? e.message : "Erro inesperado."));
  }, []);

  function renderizarLista() {
    if (erro) return <p className="text-center" role="alert">{erro}</p>;
    if (formularios === null) return <p className="text-center">Carregando...</p>;
    if (formularios.length === 0) return <p className="text-center">Nenhum formulário disponível.</p>;

    return (
      <ul className="flex flex-col gap-4 lg:gap-5">
        {formularios.map((formulario) => (
          <li
            key={formulario.id}
            className="flex items-center justify-between gap-3 rounded-md bg-card px-4 py-4 text-card-foreground lg:px-6"
          >
            <span className="min-w-0 flex-1 text-center break-words lg:text-lg">{formulario.title}</span>
            <Button asChild size="lg" className="shrink-0">
              <a
                href={formulario.url}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={`Acessar ${formulario.title} (abre em nova aba)`}
              >
                Acessar <ArrowRight aria-hidden />
              </a>
            </Button>
          </li>
        ))}
      </ul>
    );
  }

  return (
    <>
      <PageBanner
        titulo="Formulários"
        subtitulo="fonte de estudo teórico da veterinária"
        icone={<FileText />}
        ilustracao={<ClipboardList />}
      />

      <div className="mx-auto grid w-full max-w-7xl gap-8 px-4 py-8 sm:px-6 lg:grid-cols-[2fr_3fr] lg:items-center lg:gap-16 lg:px-14 lg:py-14">
        <img
          src={filhotes}
          alt="Três filhotes de cachorro"
          className="h-52 w-full rounded-2xl object-cover shadow-lg lg:aspect-square lg:h-auto"
        />
        <section aria-live="polite" className="min-w-0">{renderizarLista()}</section>
      </div>
    </>
  );
}
