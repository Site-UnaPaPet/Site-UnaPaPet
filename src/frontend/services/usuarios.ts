// Usuários (só admin). Aqui o admin escolhe o role; no cadastro público (auth.ts) a conta nasce sempre "member".
import { criarCrud } from "./api";

export type Papel = "admin" | "member";

export interface Usuario {
  id: number;
  email: string;
  role: Papel;
}

export interface NovoUsuario {
  email: string;
  password: string; // de 8 a 72 caracteres
  role?: Papel; // padrão "member"
}

export type AtualizarUsuario = Partial<NovoUsuario>;

export const usuariosAdmin = criarCrud<Usuario, NovoUsuario, AtualizarUsuario>("/admin/users");
