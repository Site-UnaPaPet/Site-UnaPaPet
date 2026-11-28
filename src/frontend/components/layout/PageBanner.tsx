import type { ReactNode } from "react";
import { PawPrint } from "lucide-react";

interface PageBannerProps {
  titulo: string;
  subtitulo: string;
  // Ícone grande à esquerda do título (ex.: <PawPrint />)
  icone: ReactNode;
  // Ilustração grande no canto direito (ex.: <ClipboardCheck />)
  ilustracao?: ReactNode;
}

// Faixa bege ondulada que abre toda página interna (menos a Home)
export default function PageBanner({ titulo, subtitulo, icone, ilustracao }: PageBannerProps) {
  return (
    <section className="relative isolate overflow-hidden bg-secondary text-secondary-foreground">
      {/* Ondas: a de cima e a de baixo usam a cor do fundo da página */}
      <svg aria-hidden className="absolute inset-x-0 top-0 -z-10 h-4 w-full fill-background sm:h-6" viewBox="0 0 1440 60" preserveAspectRatio="none">
        <path d="M0 0H1440V14C1100 46 700 6 0 40Z" />
      </svg>
      <svg aria-hidden className="absolute inset-x-0 bottom-0 -z-10 h-5 w-full fill-background sm:h-8" viewBox="0 0 1440 60" preserveAspectRatio="none">
        <path d="M0 60V28C320 -6 760 36 1440 10V60Z" />
      </svg>

      {/* Patinhas decorativas */}
      <PawPrint aria-hidden className="absolute top-8 left-[58%] hidden size-7 rotate-12 opacity-60 sm:block" />
      <PawPrint aria-hidden className="absolute top-6 left-[72%] size-5 -rotate-12 opacity-40" />
      <PawPrint aria-hidden className="absolute bottom-10 left-[66%] hidden size-5 rotate-6 opacity-40 sm:block" />

      <div className="mx-auto flex min-h-36 max-w-5xl items-center gap-3 px-4 py-8 sm:min-h-44 sm:gap-5 sm:px-6">
        <div aria-hidden className="shrink-0 text-primary [&>svg]:size-12 sm:[&>svg]:size-20">
          {icone}
        </div>

        <div className="min-w-0 flex-1">
          <h1 className="font-heading text-3xl text-primary sm:text-5xl">{titulo}</h1>
          <p className="font-soft mt-1 text-xs text-primary/90 sm:text-base">{subtitulo}</p>
        </div>

        {ilustracao ? (
          <div aria-hidden className="-mr-2 shrink-0 -rotate-6 text-primary [&>svg]:size-20 [&>svg]:stroke-[1.5] sm:[&>svg]:size-36">
            {ilustracao}
          </div>
        ) : null}
      </div>
    </section>
  );
}
