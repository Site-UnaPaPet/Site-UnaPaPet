// Único lugar que conversa com o backend. As páginas nunca chamam fetch direto: usam as funções de services/.
//
// Autenticação: o backend guarda o login em cookies httpOnly (access_token e refresh_token). O JavaScript não
// enxerga o token, então não há nada para guardar aqui: basta mandar `credentials: "include"` em toda chamada.
// Para isso funcionar, a variável ORIGIN do backend precisa ter a URL deste site (e não "*").

// A URL do backend vem do .env (VITE_API_URL), sem barra no final
const BASE_URL: string = (import.meta.env.VITE_API_URL ?? "").replace(/\/+$/, "");

type Metodo = "GET" | "POST" | "PUT" | "DELETE";

// Parâmetros da URL (?a=1&b=true). Os que forem undefined são ignorados.
export type Query = Record<string, string | number | boolean | undefined>;

interface Opcoes {
  corpo?: unknown;
  query?: Query;
  // Se a chamada der 401, tenta renovar o login (refresh) uma vez e repete a chamada. Padrão: true.
  renovarSeExpirar?: boolean;
}

// Erro de qualquer chamada à API. Mostre `message` para a pessoa; `status` e `detail` servem para decidir o que fazer.
export class ApiError extends Error {
  readonly status: number; // código HTTP (0 = não conseguiu falar com o servidor)
  readonly detail: string; // texto técnico que o backend devolveu (em inglês)
  readonly retryAfter?: number; // só no 429: quantos segundos esperar

  constructor(status: number, detail: string, retryAfter?: number) {
    super(mensagemParaPessoa(status, detail, retryAfter));
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
    this.retryAfter = retryAfter;
  }
}

function mensagemParaPessoa(status: number, detail: string, retryAfter?: number): string {
  if (status === 0) return "Não foi possível conectar ao servidor. Verifique sua conexão e tente de novo.";
  if (status === 401) {
    return detail === "Invalid email or password" ? "E-mail ou senha incorretos." : "Sua sessão expirou. Entre novamente.";
  }
  if (status === 403) return "Você não tem permissão para fazer isso.";
  if (status === 404) return "Não encontrado.";
  if (status === 409) {
    return detail === "Email already registered" ? "Este e-mail já está cadastrado." : "Já existe um registro com esses dados.";
  }
  if (status === 422) return "Dados inválidos. Confira os campos e tente de novo.";
  if (status === 429) return `Muitas requisições. Tente de novo em ${retryAfter ?? 60} segundos.`;
  if (status >= 500) return "Erro no servidor. Tente novamente mais tarde.";
  return `Erro inesperado (${status}).`;
}

// O backend responde {"detail": "texto"} ou, no 422, {"detail": [{loc, msg}, ...]}
function lerDetalhe(corpo: unknown): string {
  if (typeof corpo !== "object" || corpo === null || !("detail" in corpo)) return "";
  const { detail } = corpo as { detail: unknown };
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item: { loc?: unknown[]; msg?: string }) => `${(item.loc ?? []).slice(1).join(".")}: ${item.msg ?? ""}`)
      .join("; ");
  }
  return "";
}

function montarUrl(caminho: string, query?: Query): string {
  const params = new URLSearchParams();
  for (const [chave, valor] of Object.entries(query ?? {})) {
    if (valor !== undefined) params.set(chave, String(valor));
  }
  const texto = params.toString();
  return `${BASE_URL}${caminho}${texto ? `?${texto}` : ""}`;
}

// Faz o fetch. Se a rede falhar, devolve um ApiError de status 0.
async function enviar(metodo: Metodo, caminho: string, opcoes: Opcoes): Promise<Response> {
  const temCorpo = opcoes.corpo !== undefined;
  try {
    return await fetch(montarUrl(caminho, opcoes.query), {
      method: metodo,
      headers: temCorpo ? { "Content-Type": "application/json" } : undefined,
      body: temCorpo ? JSON.stringify(opcoes.corpo) : undefined,
      credentials: "include", // sem isso o navegador não envia nem guarda os cookies de login
    });
  } catch {
    throw new ApiError(0, "Network error");
  }
}

// Converte a resposta: sucesso vira o JSON (ou undefined, no 204); erro vira ApiError
async function tratar<T>(resposta: Response): Promise<T> {
  if (resposta.ok) {
    if (resposta.status === 204) return undefined as T;
    return (await resposta.json()) as T;
  }

  const corpo: unknown = await resposta.json().catch(() => null);
  const retryAfter = Number(resposta.headers.get("Retry-After")) || undefined;
  throw new ApiError(resposta.status, lerDetalhe(corpo), retryAfter);
}

// Várias chamadas podem dar 401 ao mesmo tempo: todas esperam a mesma renovação
let renovacao: Promise<boolean> | null = null;

function renovarSessao(): Promise<boolean> {
  renovacao ??= (async () => {
    try {
      return (await enviar("POST", "/auth/refresh", {})).ok;
    } catch {
      return false;
    } finally {
      renovacao = null;
    }
  })();
  return renovacao;
}

// Função genérica de requisição. Devolve o JSON da resposta já tipado.
export async function request<T>(metodo: Metodo, caminho: string, opcoes: Opcoes = {}): Promise<T> {
  if (!BASE_URL) throw new Error("VITE_API_URL não está definida. Confira o .env na raiz do projeto.");

  const resposta = await enviar(metodo, caminho, opcoes);

  // O login (access token) dura 15 minutos. Se venceu, renova pelo refresh token e tenta de novo, uma vez só.
  // As rotas /auth/* ficam de fora: um 401 nelas (ex.: senha errada) é o resultado esperado.
  if (resposta.status === 401 && opcoes.renovarSeExpirar !== false && !caminho.startsWith("/auth/")) {
    if (await renovarSessao()) return tratar<T>(await enviar(metodo, caminho, opcoes));
  }

  return tratar<T>(resposta);
}

// As 5 rotas de admin de um recurso: GET lista, GET {id}, POST, PUT {id}, DELETE {id}
export function criarCrud<Item, Novo, Mudanca = Partial<Novo>>(base: string) {
  return {
    listar: (query?: Query) => request<Item[]>("GET", base, { query }),
    buscar: (id: number) => request<Item>("GET", `${base}/${id}`),
    criar: (dados: Novo) => request<Item>("POST", base, { corpo: dados }),
    atualizar: (id: number, dados: Mudanca) => request<Item>("PUT", `${base}/${id}`, { corpo: dados }),
    apagar: (id: number) => request<void>("DELETE", `${base}/${id}`),
  };
}
