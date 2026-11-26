import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { MenuIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { cn } from "@/lib/utils";

// Itens do menu, na ordem do design
const MENU = [
  { texto: "Início", rota: "/" },
  { texto: "Calendário", rota: "/calendario" },
  { texto: "Formulários", rota: "/formularios" },
  { texto: "Presença", rota: "/presenca" },
  { texto: "Blog", rota: "/blog" },
];

// Logo em texto (a imagem do logo ainda não está em assets/)
function Logo() {
  return (
    <Link to="/" aria-label="UnaPáPet, ir para o início" className="font-heading text-2xl leading-none sm:text-3xl">
      <span className="text-brand-red">una</span>
      <span className="text-brand-brown">PáPet</span>
    </Link>
  );
}

// Estilo de cada link: o da página aberta fica numa pílula rosada
function classeDoLink({ isActive }: { isActive: boolean }) {
  return cn(
    "rounded-full px-3 py-2 text-sm font-bold text-foreground transition-colors hover:bg-accent/60",
    isActive && "bg-accent",
  );
}

export default function Header() {
  const [aberto, setAberto] = useState(false);

  return (
    <header className="bg-background">
      <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-4 py-4 sm:px-6">
        <Logo />

        {/* Telas médias e grandes: menu em linha */}
        <nav aria-label="Principal" className="hidden items-center gap-1 md:flex">
          {MENU.map((item) => (
            <NavLink key={item.rota} to={item.rota} end={item.rota === "/"} className={classeDoLink}>
              {item.texto}
            </NavLink>
          ))}
        </nav>

        {/* Celular: botão que abre o menu numa gaveta lateral */}
        <Sheet open={aberto} onOpenChange={setAberto}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon" className="md:hidden" aria-label="Abrir menu">
              <MenuIcon />
            </Button>
          </SheetTrigger>
          <SheetContent side="right" className="bg-background">
            <SheetHeader>
              <SheetTitle className="font-heading text-primary">Menu</SheetTitle>
              <SheetDescription className="sr-only">Links para as páginas do site</SheetDescription>
            </SheetHeader>
            <nav aria-label="Principal (celular)" className="flex flex-col gap-1 px-4">
              {MENU.map((item) => (
                <NavLink
                  key={item.rota}
                  to={item.rota}
                  end={item.rota === "/"}
                  onClick={() => setAberto(false)}
                  className={(estado) => cn(classeDoLink(estado), "px-4 py-3 text-base")}
                >
                  {item.texto}
                </NavLink>
              ))}
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}
