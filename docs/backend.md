# Backend — UnaPáPet

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

Backend do site do UnaPáPet, feito em **Python + FastAPI**, com banco de dados **assíncrono** (SQLAlchemy). Todo o código fica em `src/backend/`.

O desenho das tabelas está em `docs/schema.png`.

## Estrutura de pastas

```
Site-UnaPaPet/
├── .env.example              ← na raiz do projeto, antes de src/
├── Dockerfile.back
├── compose.yml
├── requirements.txt
├── .github/workflows/backend.yaml
├── docs/
└── src/
    ├── backend/
    │   ├── main.py                  ← cria o app e os comandos (make_migrate, create_admin)
    │   ├── config.py                ← lê as variáveis de ambiente
    │   ├── depends.py               ← dependências das rotas (token, admin, banco)
    │   ├── exceptions.py            ← erros do projeto
    │   ├── logs.py                  ← o logger
    │   ├── handles/                 ← as ROTAS, uma por arquivo
    │   │   ├── auth.py, admin.py, health.py
    │   │   ├── events.py, posts.py, forms.py, attendance.py
    │   │   └── committees.py, students.py, meetings.py, attendances.py, users.py
    │   ├── schema/                  ← o formato do que entra e sai de cada rota
    │   │   └── (um arquivo por rota, mesmo nome do handles/)
    │   ├── auth/
    │   │   ├── hash.py              ← senha (bcrypt)
    │   │   ├── token.py             ← JWT (create e read)
    │   │   └── manage.py            ← junta os dois (AuthManage)
    │   ├── database/
    │   │   ├── _base_.py            ← a Base do SQLAlchemy
    │   │   ├── url.py               ← decide a URL do banco
    │   │   ├── manage.py            ← ManageDb: junta conexão, migração e operations
    │   │   ├── connection/          ← engine e sessão
    │   │   ├── migration/           ← cria e apaga as tabelas
    │   │   ├── models/              ← as tabelas (uma por arquivo)
    │   │   └── operations/          ← o que se faz em cada tabela (uma por arquivo)
    │   └── midlleware/
    │       ├── midlle.py            ← rate limit
    │       ├── count.py             ← contador do rate limit
    │       └── routes.py            ← lista de rotas públicas e privadas
    └── tests/
        ├── db.py                    ← testa o banco
        ├── encode.py                ← testa hash e token
        └── api/                     ← chama todas as rotas
```

## Como as peças se conectam

```
Requisição → CORS → Midlleware (rate limit) → handles/* → depends.py → operations → models → banco
                                                  │                                    
                                                  └── schema/* (valida o que entra e o que sai)
```

1. A requisição chega no `uvicorn` e passa pelo **CORS** (quem pode chamar a API).
2. O **Midlleware** conta as requisições e devolve `429` se passou do limite.
3. O `FastAPI` escolhe a rota em `handles/` pelo método e pelo caminho.
4. O `schema/` valida o corpo da requisição e define o formato da resposta.
5. O `depends.py` confere o token (nas rotas protegidas) e entrega a `ManageOperations`.
6. A rota chama uma função de `database/operations/`, que mexe na tabela de `database/models/`.
7. Se o banco der erro, vira `DatabaseOperationError` e a API responde `409` ou `500`.

A `ManageOperations` é criada **uma vez**, quando a API liga (função `lifespan` do `main.py`), e fica em `request.state.operations`.

## O que cada arquivo deve ter

### `src/backend/` (arquivos soltos)

| Arquivo | O que deve ter | Para que serve |
|---|---|---|
| `main.py` | A classe `Server` (`add_midlleware`, `add_cors`, `add_routes` e `run`), o `lifespan`, e no fim `app = instance.run()`. Também os comandos de terminal `make_migrate` e `create_admin`. | Ponto de entrada. É o `src.backend.main:app` que o `uvicorn` roda. |
| `config.py` | A classe `Settings`, que carrega o `.env` e lê as variáveis obrigatórias (`requireds`) e opcionais (`optionals`). Faltou uma obrigatória: levanta `NotFoundEnv`. | Único lugar que lê variáveis de ambiente. |
| `depends.py` | `AuthDepends` (`get_payload` valida o token; `require_admin` exige admin) e `get_ops` (pega a `ManageOperations` do `request.state`). | Dependências que as rotas injetam com `Depends(...)`. |
| `exceptions.py` | Uma classe por erro: `NotFoundEnv`, `SettingsValueError`, `ConnectionDatabaseError`, `SessionMakeError`, `DatabaseOperationError`, `InvalidTokenError`, `InstanceNotFound`. | Erros com nome claro, para quem captura saber o que aconteceu. |
| `logs.py` | O objeto `logger`. | Todo o projeto usa o mesmo logger. |

### `handles/` (as rotas)

Cada arquivo é um `APIRouter`. Rotas públicas ficam em `router`, rotas de admin em `admin_router` (prefixo `/admin/...`, com `require_admin` no router inteiro, para não esquecer de proteger nenhuma).

| Arquivo | Prefixo | Observação |
|---|---|---|
| `auth.py` | `/auth` | Cadastro, login, refresh e logout. |
| `admin.py` | `/admin` | Só confirma que o token é de admin. |
| `health.py` | `/health` | Verificação de que a API está de pé. |
| `events.py`, `posts.py`, `forms.py` | `/events`, `/posts`, `/forms` e `/admin/...` | Leitura pública + CRUD de admin. |
| `attendance.py` | `/attendance` | Consulta pública de presença por RA. |
| `committees.py`, `students.py`, `meetings.py`, `attendances.py`, `users.py` | `/admin/...` | Só admin. |

### `schema/`

Modelos do **Pydantic**, um arquivo por rota. Cada recurso tem `Create` (corpo do `POST`), `Update` (corpo do `PUT`, campos opcionais) e `Response` (o que a API devolve). Nenhuma resposta devolve `password_hash`.

### `auth/`

| Arquivo | O que deve ter |
|---|---|
| `hash.py` | `Hash` com `generate(senha)` e `compare(senha, hash)`. Usa **bcrypt**. |
| `token.py` | `JWT` com `create(payload)` e `read(token)`. Algoritmo `HS256`. Qualquer erro vira `InvalidTokenError`. |
| `manage.py` | `AuthManage`, que junta `Hash` e `JWT` e lê o `JWT_SECRET`. |

### `database/`

| Pasta/arquivo | O que deve ter |
|---|---|
| `models/` | As tabelas (veja abaixo). O `__init__.py` importa todas, para a `Base` conhecer cada uma. |
| `operations/` | Uma classe por tabela com `create_x`, `get_x`, `list_x`, `update_x` e `delete_x`. Cada operação abre a própria transação (`async with session.begin()`), registra no logger e converte qualquer erro em `DatabaseOperationError`. O `manage.py` junta tudo em `ManageOperations`. |
| `connection/` | `engine.py` (cria a engine e testa a conexão), `session.py` (fábrica de sessões) e `manage.py` (`ManageConnect`). |
| `migration/` | `Migrate` com `create_tables()` (só cria as que não existem) e `drop_tables()`. |
| `manage.py` | `ManageDb`, com `migrate()` e `operations()`. |
| `url.py` | Escolhe a URL do banco e converte entre `sqlite`/`sqlite+aiosqlite` e `postgresql`/`postgresql+asyncpg`. |

### `midlleware/`

| Arquivo | O que deve ter |
|---|---|
| `midlle.py` | O `Midlleware`: rate limit por cliente (`RATE_LIMIT`) e global (`GLOBAL_RATE_LIMIT`), por minuto. Estourou: `429` com o cabeçalho `Retry-After`. |
| `count.py` | O `CountThread`, o contador (com janela de 1 minuto) usado pelo middleware. |
| `routes.py` | `PUBLIC_ROUTES` e `PRIVATE_ROUTES` (só caminho e método). Hoje é uma lista de referência: o middleware ainda não a usa. |

## Banco de dados

Oito tabelas (desenho em `docs/schema.png`):

| Tabela | Campos | Relação |
|---|---|---|
| `committees` | `id`, `name` (único) | 1 comitê → N alunos |
| `students` | `id`, `ra` (único), `name`, `committee_id`, `active` | 1 aluno → N presenças |
| `meetings` | `id`, `date` (único) | 1 reunião → N presenças |
| `attendances` | `id`, `student_id`, `meeting_id`, `status` | Único por (`student_id`, `meeting_id`) |
| `events` | `id`, `title`, `description`, `location`, `starts_at`, `image_url` | — |
| `posts` | `id`, `title`, `summary`, `image_url`, `published_at` | — |
| `forms` | `id`, `title`, `url`, `position`, `active` | — |
| `users` | `id`, `email` (único), `password_hash`, `role` | — |

- `status` da presença: `PRESENT`, `ABSENT` ou `EXCUSED`. Sem linha para uma reunião significa "não se aplica". Os totais são calculados por consulta, não guardados.
- `role` do usuário: `admin` ou `member`.
- Sem `URL_DB`, o banco padrão é um SQLite local. Para Postgres, use `postgresql://usuario:senha@host:5432/banco`. O `url.py` ajusta o driver sozinho.

## Variáveis de ambiente

O `.env` fica na **raiz do projeto**. Copie o `.env.example` e ajuste.

| Variável | Obrigatória? | Para que serve | Exemplo |
|---|---|---|---|
| `JWT_SECRET` | Sim | Segredo que assina os tokens. Longo e aleatório. | `python -c "import secrets; print(secrets.token_urlsafe(48))"` |
| `ORIGIN` | Sim | Origens permitidas no CORS, separadas por vírgula. `*` libera todas (só para teste). | `http://localhost:5173` |
| `RATE_LIMIT` | Sim | Requisições por minuto de cada cliente (IP). | `60` |
| `GLOBAL_RATE_LIMIT` | Sim | Requisições por minuto de todos juntos. | `1000` |
| `URL_DB` | Não | URL do banco. Sem ela, usa SQLite local. | `sqlite:///data/data.db` |
| `COOKIE_SECURE` | Não | `false` só para desenvolver em `http`. Em produção, deixe `true` (o padrão). | `false` |
| `ADMIN_EMAIL` | Só no `create_admin` | E-mail do admin criado pelo comando. | `admin@exemplo.com` |
| `ADMIN_PASSWORD` | Só no `create_admin` | Senha do admin (de 8 a 72 caracteres). | — |

> Com `ORIGIN=*` o navegador **não** envia os cookies (`access_token` e `refresh_token`) entre origens diferentes, e o login pelo site não funciona. Para o frontend usar a API, liste a origem dele (`ORIGIN=http://localhost:5173`). `*` serve só para testar com `curl` ou com os testes da API.

## Rotas

Base: `http://localhost:8000`. A documentação interativa (para testar as rotas pelo navegador) abre em **http://localhost:8000/docs**.

### Públicas (sem token)

| Método | Caminho | O que faz |
|---|---|---|
| `GET` | `/health` | Devolve `{"status": "ok"}`. |
| `POST` | `/auth/register` | Cria uma conta (sempre como `member`) e devolve o token. |
| `POST` | `/auth/login` | Entra e devolve o token. |
| `POST` | `/auth/refresh` | Gera um novo access token usando o cookie do refresh. |
| `POST` | `/auth/logout` | Apaga os cookies (`access_token` e `refresh_token`). |
| `GET` | `/events` | Lista os eventos (Calendário). |
| `GET` | `/events/{id}` | Um evento. |
| `GET` | `/posts` | Lista os posts (Blog), do mais novo ao mais antigo. |
| `GET` | `/posts/{id}` | Um post. |
| `GET` | `/forms` | Lista só os formulários ativos, ordenados por `position`. |
| `GET` | `/attendance/{ra}` | Consulta de presença de um aluno pelo RA. |

### Só admin (exigem token de admin)

Todas começam com `/admin`. Para cada recurso abaixo existem as 5 rotas padrão:

| Método | Caminho | O que faz |
|---|---|---|
| `GET` | `/admin/{recurso}` | Lista. |
| `POST` | `/admin/{recurso}` | Cria (`201`). |
| `GET` | `/admin/{recurso}/{id}` | Um item. |
| `PUT` | `/admin/{recurso}/{id}` | Atualiza. |
| `DELETE` | `/admin/{recurso}/{id}` | Apaga (`204`). |

`{recurso}` pode ser: `events`, `posts`, `forms`, `committees`, `students`, `meetings`, `attendances` ou `users`. Mais a rota `GET /admin`, que confirma o token de admin e devolve `{"id": ..., "role": "admin"}`.

Filtros opcionais na lista:
- `GET /admin/students?committee_id=1&only_active=true`
- `GET /admin/attendances?student_id=1` ou `?meeting_id=1`

Os campos de cada recurso, com os limites, exemplos de corpo e de resposta, estão na seção **Referência detalhada das rotas**, mais abaixo.

### Códigos de resposta

| Código | Quando |
|---|---|
| `200` / `201` / `204` | Deu certo (`201` ao criar, `204` ao apagar). |
| `401` | Sem token, token inválido ou expirado, ou login errado. |
| `403` | Token válido, mas o usuário não é admin. |
| `404` | Item não encontrado. |
| `409` | Conflito: já existe (RA, e-mail, nome, data ou presença repetidos). |
| `422` | Corpo inválido (campo faltando, senha curta, e-mail mal formado). |
| `429` | Muitas requisições. O cabeçalho `Retry-After` diz quantos segundos esperar. |
| `500` | Erro no banco (sem detalhes na resposta, só no log). |

## Referência detalhada das rotas

Tudo o que precisa para chamar cada rota: método, caminho, headers, parâmetros, corpo, resposta e erros possíveis.

### Convenções gerais

**Base:** `http://localhost:8000`. Os corpos de requisição e de resposta são sempre **JSON** (UTF-8).

#### Headers da requisição

| Header | Quando enviar | Valor |
|---|---|---|
| `Content-Type` | Em toda requisição **com corpo** (`POST` e `PUT`) | `application/json` |
| `Cookie` | Em toda rota protegida (`/admin/...`) e em `POST /auth/refresh` | `access_token=...` e `refresh_token=...`. **O navegador manda sozinho**, se a chamada usar `credentials: "include"`. É o jeito padrão do site. |
| `Authorization` | Alternativa ao cookie, para clientes que não são navegador (`curl`, testes, outros programas) | `Bearer <access_token>`. Se vierem os dois, vale o `Authorization`. |
| `Origin` | O navegador envia sozinho | Precisa estar na variável `ORIGIN` do backend (ou ela ser `*`). |

O CORS só aceita os headers `Authorization` e `Content-Type` e os métodos `GET`, `POST`, `PUT` e `DELETE`. Qualquer outro header customizado é barrado pelo navegador.

#### Headers da resposta

| Header | Quando aparece |
|---|---|
| `Set-Cookie` | Em `register`, `login` e `refresh` (grava os dois cookies) e em `logout` (apaga os dois). `access_token`: `HttpOnly`, `Path=/`, `SameSite=Lax`, `Max-Age=900` (15 minutos). `refresh_token`: `HttpOnly`, `Path=/auth`, `SameSite=Lax`, `Max-Age=604800` (7 dias). Os dois levam `Secure`, a não ser que `COOKIE_SECURE=false`. |
| `WWW-Authenticate: Bearer` | Em toda resposta `401` de rota com token. |
| `Retry-After: <segundos>` | Em toda resposta `429` (quanto esperar). |
| `access-control-allow-origin` e outros de CORS | Quando a requisição traz `Origin` permitido. |

#### Tipos dos campos

| Tipo | Formato | Exemplo |
|---|---|---|
| `id` | Inteiro, gerado pela API. Nas URLs (`{id}`), um valor que não é inteiro responde `422`. | `7` |
| data | `AAAA-MM-DD` | `"2026-11-25"` |
| data e hora | ISO 8601, **sem fuso**. A API devolve no mesmo formato. | `"2026-12-01T10:00:00"` |
| booleano | `true` ou `false` (sem aspas) | `true` |
| texto opcional | Pode ser omitido ou `null` | `null` |

#### Formato dos erros

Toda resposta de erro tem um corpo JSON com a chave `detail`.

```json
{"detail": "Event not found"}
```

O `422` (corpo inválido) traz uma **lista**, com um item por campo errado:

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "String should have at least 8 characters",
      "input": "123",
      "ctx": {"min_length": 8}
    }
  ]
}
```

`loc` diz onde está o erro (`body`, `query` ou `path`) e qual campo.

| Status | `detail` | Quando |
|---|---|---|
| `401` | `Not authenticated` | Faltou o cookie `access_token` e o header `Authorization: Bearer ...`. |
| `401` | `Invalid or expired token` | Token adulterado, expirado, ou um refresh token usado como access token. |
| `403` | `Admin only` | Token válido, mas o usuário não é admin. |
| `404` | `<Recurso> not found` | O `id` (ou RA) não existe. Ex.: `Event not found`. |
| `409` | `Conflict with existing data` | Valor repetido onde precisa ser único (RA, nome de comitê, data de reunião, presença do mesmo aluno na mesma reunião...). |
| `409` | `Email already registered` | E-mail já cadastrado (em `register` e em `POST /admin/users`). |
| `422` | lista (acima) | Campo faltando, tipo errado, tamanho fora do limite. |
| `429` | `Too many requests` | Passou do limite de requisições. Veja o header `Retry-After`. |
| `500` | `Database error` | Falha inesperada no banco. Os detalhes só aparecem no log do servidor. |

#### Exemplo com `fetch` (frontend)

```js
const API = "http://localhost:8000";

// 1. login: o servidor grava os cookies httpOnly (o JavaScript nem enxerga o token)
await fetch(`${API}/auth/login`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  credentials: "include",                       // obrigatório: sem isso o navegador ignora os cookies
  body: JSON.stringify({ email: "admin@exemplo.com", password: "senha-do-admin" }),
});

// 2. rota protegida: não precisa de header de autenticação, o cookie vai sozinho
const res = await fetch(`${API}/admin/events`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  credentials: "include",
  body: JSON.stringify({ title: "Feira de adoção", starts_at: "2026-12-01T10:00:00" }),
});
if (!res.ok) throw new Error((await res.json()).detail);   // 401, 403, 409, 422...

// 3. se vier 401, renove os cookies (sem corpo) e repita a chamada
await fetch(`${API}/auth/refresh`, { method: "POST", credentials: "include" });

// 4. sair: apaga os cookies
await fetch(`${API}/auth/logout`, { method: "POST", credentials: "include" });
```

---

### Saúde

#### `GET /health`

- **Acesso:** público. **Headers:** nenhum. **Corpo:** nenhum.
- **Resposta `200`:**
```json
{"status": "ok"}
```

---

### Autenticação (`/auth`)

Os tokens são JWT. O **access token** vale 15 minutos e leva `sub` (id do usuário), `role` e `type: "access"`. O **refresh token** vale 7 dias e leva `sub` e `type: "refresh"`. Os dois são gravados em **cookies `httpOnly`** (o JavaScript do site não consegue ler). O access token também vem no corpo da resposta, para clientes que não usam cookie (`curl`, testes).

#### `POST /auth/register`

Cria uma conta. A conta nasce **sempre como `member`**: se mandar `role` no corpo, ele é ignorado.

- **Acesso:** público.
- **Headers:** `Content-Type: application/json`

| Campo | Tipo | Obrigatório | Regras |
|---|---|---|---|
| `email` | texto | sim | Até 255 caracteres, no formato `algo@dominio.com`. |
| `password` | texto | sim | De 8 a 72 caracteres (o bcrypt usa no máximo 72 **bytes**, e letras com acento ocupam mais de 1). |

**Requisição:**
```json
{"email": "ana@exemplo.com", "password": "senha12345"}
```

**Resposta `201`:** e os headers `Set-Cookie: access_token=...` e `Set-Cookie: refresh_token=...`
```json
{"id": 4, "email": "ana@exemplo.com", "access_token": "eyJhbGciOi...", "token_type": "bearer"}
```

**Erros:** `409` (`Email already registered`), `422` (e-mail mal formado, senha curta).

#### `POST /auth/login`

- **Acesso:** público.
- **Headers:** `Content-Type: application/json`

| Campo | Tipo | Obrigatório | Regras |
|---|---|---|---|
| `email` | texto | sim | Até 255 caracteres, formato de e-mail. |
| `password` | texto | sim | De 1 a 72 caracteres. |

**Requisição:**
```json
{"email": "admin@exemplo.com", "password": "senha-do-admin"}
```

**Resposta `200`:** e os headers `Set-Cookie: access_token=...` e `Set-Cookie: refresh_token=...`
```json
{"access_token": "eyJhbGciOi...", "token_type": "bearer"}
```

**Erros:** `401` (`Invalid email or password`, a mesma mensagem para e-mail inexistente e senha errada), `422`.

#### `POST /auth/refresh`

Troca o refresh token por um access token novo e **gira** os dois (devolve dois cookies novos).

- **Acesso:** precisa do cookie `refresh_token` (não usa `Authorization`).
- **Headers:** nenhum obrigatório. No navegador, use `credentials: "include"`. Em `curl`, use `-b cookies.txt`.
- **Corpo:** nenhum.

**Resposta `200`:** e novos `Set-Cookie: access_token=...` e `Set-Cookie: refresh_token=...`
```json
{"access_token": "eyJhbGciOi...", "token_type": "bearer"}
```

**Erros:** `401` (`Invalid or expired refresh token`): sem cookie, cookie inválido ou vencido, ou o usuário foi apagado.

O cookie `refresh_token` tem `Path=/auth`, então o navegador só o envia para rotas `/auth/...`. Já o `access_token` tem `Path=/` e vai em todas as rotas.

#### `POST /auth/logout`

- **Acesso:** público (não precisa de token). **Corpo:** nenhum.
- **Resposta `204`:** sem corpo, e dois `Set-Cookie` com `Max-Age=0` (apagam o `access_token` e o `refresh_token`).

O logout só apaga os cookies: ele **não invalida** os tokens no servidor (veja as pendências no fim).

---

### Rota de admin (`/admin`)

#### `GET /admin`

Confirma que o token é de um admin e devolve quem é. Serve para o frontend decidir se mostra o painel.

- **Acesso:** admin.
- **Headers:** o cookie `access_token` (o navegador manda sozinho) **ou** `Authorization: Bearer <access_token>`
- **Resposta `200`:**
```json
{"id": 1, "role": "admin"}
```
- **Erros:** `401` (sem token, token inválido ou vencido), `403` (`Admin only`).

---

### Rotas públicas de leitura

Sem `Authorization` e sem corpo. Nenhuma tem paginação: a lista vem inteira.

#### `GET /events`

Lista os eventos, do mais próximo ao mais distante (`starts_at` crescente).

**Resposta `200`:**
```json
[
  {
    "id": 1,
    "title": "Feira de adoção",
    "description": null,
    "location": "Campus",
    "starts_at": "2026-12-01T10:00:00",
    "image_url": null
  }
]
```

#### `GET /events/{id}`

Um evento, no mesmo formato de um item acima. **Erros:** `404` (`Event not found`), `422` (`id` que não é inteiro).

#### `GET /posts`

Lista os posts, do mais novo ao mais antigo (`published_at` decrescente).

**Resposta `200`:**
```json
[
  {
    "id": 1,
    "title": "Novidade",
    "summary": "Resumo do post",
    "image_url": null,
    "published_at": "2026-11-01T10:00:00"
  }
]
```

#### `GET /posts/{id}`

Um post. **Erros:** `404` (`Post not found`).

#### `GET /forms`

Lista **só os formulários ativos** (`active: true`), ordenados por `position`.

**Resposta `200`:**
```json
[
  {"id": 1, "title": "Inscrição", "url": "https://exemplo.com/form", "position": 1, "active": true}
]
```

#### `GET /attendance/{ra}`

Consulta a presença de um aluno pelo RA.

- **Parâmetro de caminho:** `ra` (texto), por exemplo `/attendance/123456`.
- **Resposta `200`:** os totais por status e a lista de reuniões, da mais antiga para a mais nova.
```json
{
  "name": "Ana",
  "present": 3,
  "absent": 1,
  "excused": 0,
  "meetings": [
    {"date": "2026-11-01", "status": "PRESENT"},
    {"date": "2026-11-08", "status": "ABSENT"}
  ]
}
```
- **Erros:** `404` (`Student not found`). É a mesma resposta para RA inexistente e para aluno inativo, de propósito, para não dar pistas.
- Não devolve id, RA nem comitê. Só entram reuniões em que o aluno tem presença registrada.

---

### Rotas de admin (CRUD)

Valem para os 8 recursos: `events`, `posts`, `forms`, `committees`, `students`, `meetings`, `attendances` e `users`. **Todas exigem** o token de um admin (cookie `access_token` ou `Authorization: Bearer <access_token>`) (erros `401` e `403` em qualquer uma).

#### O padrão das 5 rotas

| Método e caminho | Corpo | Resposta de sucesso | Erros |
|---|---|---|---|
| `GET /admin/{recurso}` | — | `200` e uma **lista** de itens | — |
| `POST /admin/{recurso}` | campos do recurso (`Create`) | `201` e o item criado, com o `id` | `409`, `422` |
| `GET /admin/{recurso}/{id}` | — | `200` e o item | `404` |
| `PUT /admin/{recurso}/{id}` | campos a mudar (`Update`) | `200` e o item já atualizado | `404`, `409`, `422` |
| `DELETE /admin/{recurso}/{id}` | — | `204` **sem corpo** | `404` |

Headers: o cookie `access_token` (ou `Authorization`) em todas, e `Content-Type: application/json` no `POST` e no `PUT`.

**Como o `PUT` funciona:**
- Envie **só os campos que quer mudar**. Os que não vierem continuam como estão.
- Campos de texto opcionais (`description`, `location`, `image_url`, `summary`) aceitam `null` para limpar o valor.
- **Não envie `null` em campo obrigatório** (como `title`): o banco recusa e a resposta é `409`.
- Exceções: em `committees`, `meetings` e `attendances` o `PUT` tem **um único campo, obrigatório** (`name`, `date` e `status`, respectivamente).

**Apagar:** apagar um item que outro ainda usa (por exemplo um comitê que tem alunos) pode dar `409` em bancos que impõem a chave estrangeira, como o Postgres. Apague os filhos antes: presenças, depois alunos e reuniões, depois comitês.

---

#### `events` (`/admin/events`)

| Campo | Tipo | `POST` | Regras |
|---|---|---|---|
| `title` | texto | obrigatório | De 1 a 150 caracteres. |
| `starts_at` | data e hora | obrigatório | Ex.: `"2026-12-01T10:00:00"`. |
| `description` | texto | opcional | Sem limite. |
| `location` | texto | opcional | Até 150 caracteres. |
| `image_url` | texto | opcional | Até 500 caracteres. |

`PUT`: todos opcionais. A lista vem ordenada por `starts_at`. A resposta tem o mesmo formato do `GET /events`.

```json
{"title": "Feira de adoção", "starts_at": "2026-12-01T10:00:00", "location": "Campus"}
```

#### `posts` (`/admin/posts`)

| Campo | Tipo | `POST` | Regras |
|---|---|---|---|
| `title` | texto | obrigatório | De 1 a 150 caracteres. |
| `published_at` | data e hora | obrigatório | Ex.: `"2026-11-01T10:00:00"`. |
| `summary` | texto | opcional | Sem limite. |
| `image_url` | texto | opcional | Até 500 caracteres. |

`PUT`: todos opcionais. A lista vem do mais novo ao mais antigo. Aqui a lista de admin traz todos os posts, igual à pública.

```json
{"title": "Novidade", "published_at": "2026-11-01T10:00:00", "summary": "Resumo do post"}
```

#### `forms` (`/admin/forms`)

| Campo | Tipo | `POST` | Regras |
|---|---|---|---|
| `title` | texto | obrigatório | De 1 a 150 caracteres. |
| `url` | texto | obrigatório | De 1 a 500 caracteres. |
| `position` | inteiro | opcional | Padrão `0`. Define a ordem na lista pública. |
| `active` | booleano | opcional | Padrão `true`. Só os ativos aparecem em `GET /forms`. |

`PUT`: todos opcionais. A lista de **admin** traz também os formulários inativos.

```json
{"title": "Inscrição", "url": "https://exemplo.com/form", "position": 1, "active": true}
```

#### `committees` (`/admin/committees`)

| Campo | Tipo | `POST` | `PUT` | Regras |
|---|---|---|---|---|
| `name` | texto | obrigatório | **obrigatório** | De 1 a 80 caracteres. **Único**: nome repetido dá `409`. |

```json
{"name": "Comunicação"}
```
Resposta: `{"id": 1, "name": "Comunicação"}`. A lista vem em ordem alfabética.

#### `students` (`/admin/students`)

| Campo | Tipo | `POST` | Regras |
|---|---|---|---|
| `ra` | texto | obrigatório | De 1 a 50 caracteres. **Único**: RA repetido dá `409`. |
| `name` | texto | obrigatório | De 1 a 80 caracteres. |
| `committee_id` | inteiro | obrigatório | `id` de um comitê. |
| `active` | booleano | opcional | Padrão `true`. Aluno inativo não aparece na consulta pública por RA. |

`PUT`: todos opcionais.

```json
{"ra": "123456", "name": "Ana", "committee_id": 1, "active": true}
```
Resposta: `{"id": 1, "ra": "123456", "name": "Ana", "committee_id": 1, "active": true}`.

**Filtros na lista** (opcionais, na URL):

| Parâmetro | Tipo | Efeito |
|---|---|---|
| `committee_id` | inteiro | Só os alunos desse comitê. |
| `only_active` | booleano (`true`/`false`) | `true` devolve só os ativos. Padrão `false`. |

Exemplo: `GET /admin/students?committee_id=1&only_active=true`. A lista vem em ordem alfabética pelo nome.

> No SQLite, um `committee_id` que não existe pode ser aceito (ele não confere a chave estrangeira). No Postgres dá `409`.

#### `meetings` (`/admin/meetings`)

| Campo | Tipo | `POST` | `PUT` | Regras |
|---|---|---|---|---|
| `date` | data | obrigatório | **obrigatório** | `AAAA-MM-DD`. **Única**: não existem duas reuniões na mesma data (`409`). |

```json
{"date": "2026-11-25"}
```
Resposta: `{"id": 1, "date": "2026-11-25"}`. A lista vem em ordem de data.

#### `attendances` (`/admin/attendances`)

Registra se um aluno esteve (ou não) em uma reunião.

| Campo | Tipo | `POST` | `PUT` | Regras |
|---|---|---|---|---|
| `student_id` | inteiro | obrigatório | não existe | `id` de um aluno. |
| `meeting_id` | inteiro | obrigatório | não existe | `id` de uma reunião. |
| `status` | texto | obrigatório | **obrigatório** | Exatamente `"PRESENT"`, `"ABSENT"` ou `"EXCUSED"` (maiúsculas). |

Só pode haver **uma presença por aluno em cada reunião**: repetir o par dá `409`. No `PUT` só se muda o `status`.

```json
{"student_id": 1, "meeting_id": 1, "status": "PRESENT"}
```
Resposta: `{"id": 1, "student_id": 1, "meeting_id": 1, "status": "PRESENT"}`.

**Filtros na lista** (opcionais; se mandar os dois, vale só `student_id`):

| Parâmetro | Tipo | Efeito |
|---|---|---|
| `student_id` | inteiro | Só as presenças desse aluno. |
| `meeting_id` | inteiro | Só as presenças dessa reunião. |

Exemplo: `GET /admin/attendances?student_id=1`.

#### `users` (`/admin/users`)

Aqui, ao contrário do `register`, o admin **escolhe o `role`**.

| Campo | Tipo | `POST` | Regras |
|---|---|---|---|
| `email` | texto | obrigatório | Até 255 caracteres, formato de e-mail. **Único**. |
| `password` | texto | obrigatório | De 8 a 72 caracteres. É guardada só como hash bcrypt. |
| `role` | texto | opcional | `"admin"` ou `"member"`. Padrão `"member"`. |

`PUT`: todos opcionais. Mandar `password` troca a senha (a nova é convertida em hash antes de salvar).

```json
{"email": "novo@exemplo.com", "password": "senha12345", "role": "admin"}
```
Resposta: `{"id": 5, "email": "novo@exemplo.com", "role": "admin"}`. **Nunca** devolve a senha nem o hash.

Erros próprios: `409` (`Email already registered`) no `POST`. Num `PUT` com e-mail que já existe, o `409` vem como `Conflict with existing data`.

O `role` vai dentro do token: um usuário rebaixado continua admin até o access token vencer (no máximo 15 minutos).

**Cookies nas rotas de usuário:**
- `POST /admin/users` **não** mexe nos cookies de quem chamou: o admin continua logado como admin. Quem grava os cookies de login é o `POST /auth/register` (a pessoa criando a própria conta) e o `POST /auth/login`.
- `DELETE /admin/users/{id}`: se o admin apagar **a própria conta** (o `id` é o dele), a resposta `204` já apaga os cookies `access_token` e `refresh_token` no navegador. Se apagar outro usuário, os cookies do admin ficam como estão.
- Os cookies de outra pessoa ficam no navegador dela, e o servidor não consegue apagá-los. Como o token é um JWT sem registro no banco, quem foi apagado ainda usa o access token por até 15 minutos. Já o `POST /auth/refresh` falha na hora (`401`), porque confere se o usuário ainda existe.

---

### Limite de requisições (todas as rotas)

Cada IP pode fazer `RATE_LIMIT` requisições por minuto, e todos os clientes juntos, `GLOBAL_RATE_LIMIT`. Passou: resposta `429` com `{"detail": "Too many requests"}` e o header `Retry-After` (em segundos). Espere esse tempo e repita a chamada.

## Autenticação

- **Cadastro e login** gravam **dois cookies `httpOnly`** (o JavaScript do site não consegue lê-los): o `access_token` e o `refresh_token`. O access token também vem no corpo da resposta, para clientes que não usam cookie.
- O **access token** vale **15 minutos**. O navegador o manda sozinho no cookie (`credentials: "include"`); outros clientes podem mandar no cabeçalho `Authorization: Bearer <access_token>` (se vierem os dois, vale o cabeçalho).
- O **refresh token** vale **7 dias** e só viaja nas rotas `/auth/...`. Quando o access vencer, chame `POST /auth/refresh` e receba os dois cookies novos.
- O `POST /auth/logout` apaga os dois cookies.
- Os cookies usam `SameSite=Lax`, que bloqueia o envio em requisições vindas de outros sites (proteção contra CSRF). O site e a API precisam estar no mesmo site (por exemplo, `localhost:5173` e `localhost:8000`) ou no mesmo domínio.
- O `/auth/register` **ignora** o `role` do corpo: a conta nasce sempre como `member`. Só quem já é admin promove alguém, em `PUT /admin/users/{id}`.
- Senhas são guardadas só como hash **bcrypt**. A senha precisa ter de 8 a 72 caracteres.
- Mensagens de login não dizem se o e-mail existe: e-mail inexistente e senha errada respondem igual.

### Consulta de presença (`GET /attendance/{ra}`)

É a rota pública mais sensível, porque o RA identifica um aluno. Ela devolve só o mínimo:

```json
{
  "name": "Ana",
  "present": 3,
  "absent": 1,
  "excused": 0,
  "meetings": [{"date": "2026-11-01", "status": "PRESENT"}]
}
```

RA inexistente e RA de aluno inativo respondem o mesmo `404`, sem dar pistas. Não devolve id, RA nem comitê.

## Como usar (exemplos com `curl`)

```bash
# Ver se a API está de pé
curl http://localhost:8000/health

# Criar conta (grava os cookies e também devolve o access_token no corpo)
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "ana@exemplo.com", "password": "senha12345"}'

# Entrar: o -c guarda os cookies (access_token e refresh_token) no arquivo cookies.txt
curl -X POST http://localhost:8000/auth/login \
  -c cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@exemplo.com", "password": "senha-do-admin"}'

# Usar numa rota de admin: o -b manda os cookies guardados (igual ao navegador)
curl -X POST http://localhost:8000/admin/events \
  -b cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"title": "Feira de adoção", "starts_at": "2026-12-01T10:00:00", "location": "Campus"}'

# Alternativa sem cookie: mande o access_token (que vem no corpo do login) no cabeçalho
curl http://localhost:8000/admin \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"

# Listar eventos (público, sem token)
curl http://localhost:8000/events

# Consultar presença por RA (público)
curl http://localhost:8000/attendance/123456
```

No navegador (frontend), chame **sempre** com `credentials: "include"` (em toda rota, não só nas `/auth/...`), para os cookies irem e voltarem. Com `curl`, use `-c cookies.txt` ao entrar e `-b cookies.txt` nas chamadas seguintes, ou o cabeçalho `Authorization`.

## Como rodar

Em qualquer forma, o primeiro passo é o mesmo: na **raiz do projeto**, copie o `.env.example` para `.env` e preencha as variáveis.

```bash
cp .env.example .env
```

### Forma 1: Python puro (sem Docker)

Precisa do Python 3.14.

```bash
python -m venv .venv
source .venv/bin/activate          # no Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m src.backend.main make_migrate     # cria as tabelas (só as que não existem)
python -m src.backend.main create_admin     # cria o admin (usa ADMIN_EMAIL e ADMIN_PASSWORD)

python -m uvicorn src.backend.main:app --reload --port 8000
```

- Rode sempre **da raiz do projeto**, senão o Python não acha o pacote `src`.
- O `create_admin` pode rodar quantas vezes quiser: se o admin já existe, não faz nada.
- O `--reload` reinicia a API ao salvar um arquivo.
- Para parar, `Ctrl + C`.

### Forma 2: Docker Compose (`compose.yml`)

```bash
docker compose up --build      # constrói e sobe (veja os logs no terminal)
docker compose up -d           # sobe em segundo plano
docker compose logs -f         # acompanha os logs
docker compose down            # para e remove os containers
```

- O serviço do backend se chama `backend` e usa o `Dockerfile.back`. Ao subir, o container faz **três coisas em ordem**: cria as tabelas, cria o admin e liga o servidor. Cada passo só roda se o anterior deu certo.
- O `.env` da raiz é lido pelo Compose (`env_file`). Por isso `ADMIN_EMAIL` e `ADMIN_PASSWORD` precisam estar nele.
- Depois de mudar o código ou o `Dockerfile.back`, use `docker compose up --build`. Só `up` reaproveita a imagem antiga.
- O frontend (`interface`) só sobe depois que o backend responder `/health`.
- Se o `URL_DB` for um SQLite dentro do container, o banco **some** quando o container é recriado. Para guardar os dados, monte um volume (`volumes: - ./data:/app/data`) ou use um Postgres.

### Qual usar?

| Forma | Quando usar |
|---|---|
| Python puro | No dia a dia do backend: é a mais rápida e recarrega ao salvar. |
| Compose | Para subir backend e frontend juntos, do mesmo jeito em qualquer máquina. |

## Testes

Todos rodam **da raiz do projeto**.

| Comando | O que testa |
|---|---|
| `python -m src.tests.db` | O banco: cria as tabelas, testa todos os métodos das operations na ordem e apaga as tabelas no fim. |
| `python -m src.tests.encode` | `AuthManage`: hash (`generate`, `compare`) e token (`create`, `read`, tokens inválidos). Usa um `JWT_SECRET` de teste. |
| `python -m src.tests.api.main` | A API: chama todas as rotas em `localhost:8000`. |

> **Cuidado:** o `src.tests.db` **apaga todas as tabelas** do banco do `URL_DB` no final. Aponte só para um banco de teste.

### Testes da API (`src/tests/api/`)

- **Só fazem as requisições.** Qualquer resposta com status `>= 400` levanta o erro e mostra método, URL, status e corpo.
- Um arquivo por rota. O `main.py` acha os arquivos da pasta (menos ele e o `client.py`) e roda o `run` de cada um e depois o `delete`, na ordem inversa. Um arquivo novo entra sozinho; se ele depender de dados de outro teste, coloque o nome na lista `ORDER` do `main.py`.
- **Não mexem no banco.** A API precisa estar rodando, e o admin do `ADMIN` (em `main.py`) precisa **já existir** nela (o `create_admin` cria).
- **Simulam o navegador com cookies.** O `Client` (em `client.py`) guarda os cookies que a API manda e os reenvia sozinho. O `main.py` faz o login do admin **uma vez** (`admin.login(ADMIN)`): a API grava o `access_token` no cookie desse cliente, e todas as rotas `/admin/...` são chamadas por ele **sem** cabeçalho `Authorization`. Os testes de `/auth` usam outro cliente, para o login e o logout deles não derrubarem a sessão do admin.
- **Também testam o cabeçalho.** O `admin.py` chama `GET /admin` das duas formas: só com o cookie, e com um cliente novo mandando `Authorization: Bearer` (o `access_token` vem no corpo do login).
- **A API precisa estar com `COOKIE_SECURE=false`.** O teste fala `http`, e o cliente não envia cookie `Secure` por `http`. Com `COOKIE_SECURE=true` o teste para em `POST /auth/refresh` com `401`.
- A URL é `http://localhost:8000`. Para outra porta, use `API_URL=http://localhost:8001 python -m src.tests.api.main`.
- Uma rodada faz umas 70 requisições. Se o `RATE_LIMIT` for menor que isso, o teste espera o `Retry-After` e continua (pode demorar). Para rodar rápido, suba a API com um `RATE_LIMIT` maior.

### CI (GitHub Actions)

O arquivo `.github/workflows/backend.yaml` roda a cada push e PR para `main` e `develop`: instala as dependências e roda `src.tests.db` e `src.tests.encode`. As variáveis de ambiente do `.env` estão escritas no próprio arquivo, com valores de teste (sem `secrets`).

## Regras

### Estrutura
- **Não crie pastas nem arquivos fora desta estrutura sem combinar com o time.**
- **Rota nova, na ordem:**
  1. `database/models/`: a tabela (e importe no `models/__init__.py`);
  2. `database/operations/`: as operações (e herde na `ManageOperations`);
  3. `schema/`: `Create`, `Update` e `Response`;
  4. `handles/`: o `APIRouter`;
  5. `main.py`: coloque o router na lista de `add_routes`;
  6. `midlleware/routes.py`: acrescente o caminho e o método;
  7. `tests/api/`: um arquivo com `run` (e `delete`).
- **Rota de admin** usa o router com `dependencies=[Depends(auth_depends.require_admin)]`, e não protege rota por rota.

### Código
- **Nomes:** arquivos em `minusculo.py`, classes em `PascalCase`, funções e variáveis em `snake_case`.
- **Tudo assíncrono** nas rotas e nas operations (`async def` e `await`).
- **A rota nunca fala direto com o banco.** Sempre passa por uma função de `operations/`.
- **Toda operação registra no `logger`** (começou, deu certo, não achou, falhou).
- **Erro de banco** sempre vira `DatabaseOperationError`; a rota não precisa capturar (o `main.py` trata).
- **Tipe tudo:** parâmetros, retornos e os `schema`. A resposta usa `response_model`, para nunca vazar campo a mais.

### Segurança
- **Nunca devolva `password_hash`**, nem coloque senha ou token em log.
- **Nunca aceite `role` no cadastro público.**
- **Variáveis de ambiente só pelo `Settings`.** Nada de segredo escrito no código.
- **Nunca commite o `.env`**, só o `.env.example`.
- **Dados de alunos (RA, presença) são sensíveis:** devolva só o necessário e não registre em log.

### Git
- Trabalhe em branch própria (ex.: `feature/rota-eventos`) e abra PR para `develop`.
- Commits pequenos e com mensagem clara (`feat:`, `fix:`, `docs:`).

## Problemas comuns

- **`ModuleNotFoundError: No module named 'src'`:** você rodou fora da raiz do projeto. Rode da raiz, com `python -m ...`.
- **`NotFoundEnv: Expeted env ...`:** falta uma variável obrigatória no `.env` (veja a tabela de variáveis). O `ORIGIN` e o `JWT_SECRET` são exigidos já ao importar o `main.py`.
- **`no such table: ...`:** as tabelas não foram criadas. Rode `python -m src.backend.main make_migrate`.
- **`unable to open database file`:** a pasta do SQLite não existe. Use `URL_DB=sqlite:///data/data.db` a partir da raiz do projeto.
- **Login do admin dá `401`:** o admin não existe nesse banco. Rode `python -m src.backend.main create_admin` e confira se o `ADMIN_EMAIL` e a `ADMIN_PASSWORD` são os mesmos que você está usando.
- **`429` do rate limit:** passou de `RATE_LIMIT` requisições por minuto. Espere o `Retry-After` ou aumente o limite no `.env`.
- **O navegador bloqueia a chamada (CORS):** a origem do frontend não está no `ORIGIN`.
- **Os cookies não chegam (o login pelo site "não pega"):** com `ORIGIN=*` o navegador não envia cookies entre origens. Liste a origem do frontend no `ORIGIN` (`http://localhost:5173`) e use `credentials: "include"` em todas as chamadas. Em `http` (sem HTTPS), defina `COOKIE_SECURE=false`, senão o navegador descarta os cookies.
- **No Docker, a porta 8000 já está em uso:** feche o outro processo ou troque o lado esquerdo do `ports` no `compose.yml`.

## Estado atual e pendências

- Rotas, autenticação (access + refresh), rate limit, CORS, banco, comandos e testes estão prontos.
- **O logout só apaga os cookies.** Os tokens são JWT sem registro no banco, então não dá para cancelá-los no servidor: quem copiou um deles antes pode usá-lo até vencer (15 minutos o access, 7 dias o refresh).
- **O `role` vai dentro do token.** Um admin rebaixado continua admin até o access token vencer (15 minutos).
- **Uma sessão de banco compartilhada.** A `ManageOperations` é uma só para todas as requisições, e a `AsyncSession` do SQLAlchemy não aceita uso simultâneo. Com muitas requisições ao mesmo tempo, o ideal é uma sessão por requisição.
- **O rate limit fica na memória do processo.** Com mais de um worker, cada um conta separado.
- **O `midlleware/routes.py` ainda não é usado pelo middleware:** o limite vale igual para todas as rotas.
