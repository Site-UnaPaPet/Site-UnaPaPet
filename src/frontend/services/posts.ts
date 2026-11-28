// Posts (Home e Blog). Leitura pública + CRUD de admin.
import { criarCrud, request } from "./api";

export interface Post {
  id: number;
  title: string;
  summary: string | null;
  image_url: string | null;
  published_at: string; // "2026-11-01T10:00:00"
}

export interface NovoPost {
  title: string; // de 1 a 150 caracteres
  published_at: string; // "2026-11-01T10:00:00" (sem fuso)
  summary?: string | null;
  image_url?: string | null; // até 500 caracteres
}

export type AtualizarPost = Partial<NovoPost>;

// Públicas (sem login). A lista vem do post mais novo ao mais antigo.
export const listarPosts = () => request<Post[]>("GET", "/posts");
export const buscarPost = (id: number) => request<Post>("GET", `/posts/${id}`);

// Admin: postsAdmin.listar() / .buscar(id) / .criar(dados) / .atualizar(id, dados) / .apagar(id)
export const postsAdmin = criarCrud<Post, NovoPost, AtualizarPost>("/admin/posts");
