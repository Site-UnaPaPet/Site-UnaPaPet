import { Link } from "react-router-dom";
import { ClipboardCheck, PawPrint } from "lucide-react";

import PageBanner from "@/components/layout/PageBanner";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// Subcomissões do projeto, na ordem do design. O "slug" vai na URL da consulta.
const SUBCOMISSOES = [
  { nome: "Triagem Clínica", slug: "triagem-clinica" },
  { nome: "Manejo sanitário", slug: "manejo-sanitario" },
  { nome: "Clínica e cirurgia", slug: "clinica-e-cirurgia" },
  { nome: "Acolhimento e adoção", slug: "acolhimento-e-adocao" },
  { nome: "Banco de dados", slug: "banco-de-dados" },
  { nome: "Comunicação", slug: "comunicacao" },
  { nome: "Conforto e bem-estar animal", slug: "conforto-e-bem-estar-animal" },
];

export default function Presenca() {
  return (
    <>
      <PageBanner
        titulo="Presença"
        subtitulo="acompanhe sua frequência no projeto"
        icone={<PawPrint fill="currentColor" />}
        ilustracao={<ClipboardCheck />}
      />

      <section className="mx-auto w-full max-w-2xl px-4 py-8 sm:px-6 sm:py-12">
        <Card className="rounded-3xl bg-card py-8 ring-0 sm:py-10">
          <CardHeader>
            <CardTitle className="text-center font-heading text-3xl text-card-foreground sm:text-4xl">Subcomissões</CardTitle>
          </CardHeader>

          <CardContent>
            <ul className="mx-auto flex max-w-md flex-col gap-4 sm:gap-5">
              {SUBCOMISSOES.map((subcomissao) => (
                <li key={subcomissao.slug}>
                  <Button asChild size="lg" className="h-14 w-full rounded-md text-base sm:text-lg">
                    <Link to={`/presenca/consulta?subcomissao=${subcomissao.slug}`}>{subcomissao.nome}</Link>
                  </Button>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </section>
    </>
  );
}
