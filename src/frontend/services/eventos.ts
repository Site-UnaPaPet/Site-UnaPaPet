// Eventos (Calendário). Leitura pública + CRUD de admin.
import { criarCrud, request } from "./api";

export interface Evento {
  id: number;
  title: string;
  description: string | null;
  location: string | null;
  starts_at: string; // "2026-12-01T10:00:00"
  image_url: string | null;
}

export interface NovoEvento {
  title: string; // de 1 a 150 caracteres
  starts_at: string; // "2026-12-01T10:00:00" (sem fuso)
  description?: string | null;
  location?: string | null; // até 150 caracteres
  image_url?: string | null; // até 500 caracteres
}

export type AtualizarEvento = Partial<NovoEvento>;

// Públicas (sem login). A lista vem do evento mais próximo ao mais distante.
export const listarEventos = () => request<Evento[]>("GET", "/events");
export const buscarEvento = (id: number) => request<Evento>("GET", `/events/${id}`);

// Admin: eventosAdmin.listar() / .buscar(id) / .criar(dados) / .atualizar(id, dados) / .apagar(id)
export const eventosAdmin = criarCrud<Evento, NovoEvento, AtualizarEvento>("/admin/events");
