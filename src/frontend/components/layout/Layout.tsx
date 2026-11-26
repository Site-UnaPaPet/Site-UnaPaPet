import type { ReactNode } from "react";

import Footer from "./Footer";
import Header from "./Header";

// Moldura de todas as páginas: cabeçalho, conteúdo e rodapé
export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-svh flex-col">
      <Header />
      <main className="flex-1">{children}</main>
      <Footer />
    </div>
  );
}
