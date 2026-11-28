// Consulta pública de presença por RA (tela Presença > Consulta por RA).
import { request } from "./api";

export type StatusPresenca = "PRESENT" | "ABSENT" | "EXCUSED";

export interface ReuniaoPresenca {
  date: string; // "2026-11-01"
  status: StatusPresenca;
}

export interface ConsultaPresenca {
  name: string;
  present: number;
  absent: number;
  excused: number;
  meetings: ReuniaoPresenca[]; // da mais antiga para a mais nova
}

// Dá erro 404 se o RA não existe ou o aluno está inativo (a mesma resposta, de propósito).
// Dado sensível: não coloque o RA nem o resultado em console.log.
export const consultarPresenca = (ra: string) => request<ConsultaPresenca>("GET", `/attendance/${encodeURIComponent(ra.trim())}`);
