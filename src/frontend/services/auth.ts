// Login, cadastro e sessão. O token fica em cookie httpOnly: aqui nunca aparece token.
import { ApiError, request } from "./api";

export interface Credenciais {
  email: string;
  password: string; // de 8 a 72 caracteres no cadastro
}

export interface Conta {
  id: number;
  email: string;
}

export interface QuemSou {
  id: number;
  role: "admin";
}

// Resposta do backend no cadastro (o access_token também vem nos cookies, então não é usado)
interface RespostaCadastro extends Conta {
  access_token: string;
  token_type: string;
}

// Cria a conta (sempre como "member") e já deixa a pessoa logada
export async function registrar(credenciais: Credenciais): Promise<Conta> {
  const { id, email } = await request<RespostaCadastro>("POST", "/auth/register", { corpo: credenciais });
  return { id, email };
}

// Entra na conta: o backend grava os cookies de login
export async function entrar(credenciais: Credenciais): Promise<void> {
  await request<unknown>("POST", "/auth/login", { corpo: credenciais });
}

// Renova o login pelo refresh token. As outras funções já fazem isso sozinhas quando o login vence.
export async function renovar(): Promise<void> {
  await request<unknown>("POST", "/auth/refresh");
}

// Sai da conta: o backend apaga os cookies
export async function sair(): Promise<void> {
  await request<void>("POST", "/auth/logout");
}

// Devolve quem está logado como admin. Dá erro 401 (sem login) ou 403 (não é admin).
export function buscarAdmin(): Promise<QuemSou> {
  return request<QuemSou>("GET", "/admin");
}

// true se a pessoa está logada como admin. Serve para decidir se mostra o painel.
export async function souAdmin(): Promise<boolean> {
  try {
    await buscarAdmin();
    return true;
  } catch (erro) {
    if (erro instanceof ApiError && (erro.status === 401 || erro.status === 403)) return false;
    throw erro;
  }
}
