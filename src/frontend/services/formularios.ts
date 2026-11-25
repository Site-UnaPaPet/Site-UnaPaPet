// Formulários. Leitura pública + CRUD de admin.
import { criarCrud, request } from "./api";

export interface Formulario {
  id: number;
  title: string;
  url: string;
  position: number;
  active: boolean;
}

export interface NovoFormulario {
  title: string; // de 1 a 150 caracteres
  url: string; // de 1 a 500 caracteres
  position?: number; // ordem na lista (padrão 0)
  active?: boolean; // só os ativos aparecem na lista pública (padrão true)
}

export type AtualizarFormulario = Partial<NovoFormulario>;

// Pública (sem login): só os formulários ativos, ordenados por position
export const listarFormularios = () => request<Formulario[]>("GET", "/forms");

// Admin: a lista traz também os inativos
export const formulariosAdmin = criarCrud<Formulario, NovoFormulario, AtualizarFormulario>("/admin/forms");
