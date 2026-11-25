// Alunos (só admin).
import { criarCrud, request } from "./api";

export interface Aluno {
  id: number;
  ra: string;
  name: string;
  committee_id: number;
  active: boolean;
}

export interface NovoAluno {
  ra: string; // de 1 a 50 caracteres, único
  name: string; // de 1 a 80 caracteres
  committee_id: number;
  active?: boolean; // aluno inativo não aparece na consulta pública por RA (padrão true)
}

export type AtualizarAluno = Partial<NovoAluno>;

export type FiltrosAlunos = {
  committee_id?: number; // só os alunos dessa comissão
  only_active?: boolean; // true devolve só os ativos
};

export const alunosAdmin = criarCrud<Aluno, NovoAluno, AtualizarAluno>("/admin/students");

// Lista com filtros opcionais: listarAlunos({ committee_id: 1, only_active: true })
export const listarAlunos = (filtros?: FiltrosAlunos) => request<Aluno[]>("GET", "/admin/students", { query: filtros });
