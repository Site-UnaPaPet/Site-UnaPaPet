// Reuniões (só admin).
import { criarCrud } from "./api";

export interface Reuniao {
  id: number;
  date: string; // "2026-11-25"
}

export interface NovaReuniao {
  date: string; // "AAAA-MM-DD", única
}

export type AtualizarReuniao = NovaReuniao; // no PUT a data é obrigatória

export const reunioesAdmin = criarCrud<Reuniao, NovaReuniao, AtualizarReuniao>("/admin/meetings");
