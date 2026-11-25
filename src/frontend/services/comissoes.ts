// Comissões / subcomissões (só admin).
import { criarCrud } from "./api";

export interface Comissao {
  id: number;
  name: string;
}

export interface NovaComissao {
  name: string; // de 1 a 80 caracteres, único
}

export type AtualizarComissao = NovaComissao; // no PUT o nome é obrigatório

export const comissoesAdmin = criarCrud<Comissao, NovaComissao, AtualizarComissao>("/admin/committees");
