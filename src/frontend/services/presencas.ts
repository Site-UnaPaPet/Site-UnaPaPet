// Presenças registradas em cada reunião (só admin). Para a consulta pública por RA, veja presenca.ts.
import { criarCrud, request } from "./api";
import type { StatusPresenca } from "./presenca";

export interface Presenca {
  id: number;
  student_id: number;
  meeting_id: number;
  status: StatusPresenca;
}

export interface NovaPresenca {
  student_id: number;
  meeting_id: number;
  status: StatusPresenca;
}

export interface AtualizarPresenca {
  status: StatusPresenca; // no PUT só se muda o status (e ele é obrigatório)
}

export type FiltrosPresencas = {
  student_id?: number; // só as presenças desse aluno
  meeting_id?: number; // só as presenças dessa reunião (se mandar os dois, vale o student_id)
};

export const presencasAdmin = criarCrud<Presenca, NovaPresenca, AtualizarPresenca>("/admin/attendances");

// Lista com filtros opcionais: listarPresencas({ student_id: 1 })
export const listarPresencas = (filtros?: FiltrosPresencas) => request<Presenca[]>("GET", "/admin/attendances", { query: filtros });
