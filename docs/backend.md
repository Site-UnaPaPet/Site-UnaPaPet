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

> Com `ORIGIN=*` o navegador **não** envia o cookie do refresh token entre origens diferentes. Em produção, liste as URLs reais do site.

## Rotas

Base: `http://localhost:8000`. A documentação interativa (para testar as rotas pelo navegador) abre em **http://localhost:8000/docs**.

### Públicas (sem token)

| Método | Caminho | O que faz |
|---|---|---|
| `GET` | `/health` | Devolve `{"status": "ok"}`. |
| `POST` | `/auth/register` | Cria uma conta (sempre como `member`) e devolve o token. |
| `POST` | `/auth/login` | Entra e devolve o token. |
| `POST` | `/auth/refresh` | Gera um novo token usando o cookie do refresh. |
| `POST` | `/auth/logout` | Apaga o cookie do refresh. |
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

### Corpo de cada recurso (`POST`)

| Recurso | Campos |
|---|---|
| `events` | `title`, `starts_at`, e opcionais: `description`, `location`, `image_url` |
| `posts` | `title`, `published_at`, e opcionais: `summary`, `image_url` |
| `forms` | `title`, `url`, e opcionais: `position` (0), `active` (true) |
| `committees` | `name` |
| `students` | `ra`, `name`, `committee_id`, e opcional: `active` (true) |
| `meetings` | `date` (`AAAA-MM-DD`) |
| `attendances` | `student_id`, `meeting_id`, `status` (`PRESENT`, `ABSENT` ou `EXCUSED`) |
| `users` | `email`, `password`, e opcional: `role` (`member`; só o admin pode escolher `admin`) |

No `PUT`, envie só o que quer mudar (em `events`, `posts`, `forms`, `students` e `users`). Em `committees` o `name` é obrigatório, em `meetings` o `date` e em `attendances` o `status`.

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

## Autenticação

- **Cadastro e login** devolvem um `access_token` (JWT) e **também** gravam um `refresh_token` num cookie `httpOnly` (o JavaScript do site não consegue lê-lo).
- O **access token** vale **15 minutos** e vai no cabeçalho de toda rota protegida: `Authorization: Bearer <access_token>`.
- O **refresh token** vale **7 dias**. Quando o access vencer, chame `POST /auth/refresh` (o navegador manda o cookie sozinho) e receba um novo.
- O `POST /auth/logout` apaga o cookie.
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

# Criar conta (devolve o access_token)
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "ana@exemplo.com", "password": "senha12345"}'

# Entrar (guarde o access_token da resposta)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@exemplo.com", "password": "senha-do-admin"}'

# Usar o token numa rota de admin
curl -X POST http://localhost:8000/admin/events \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Feira de adoção", "starts_at": "2026-12-01T10:00:00", "location": "Campus"}'

# Listar eventos (público, sem token)
curl http://localhost:8000/events

# Consultar presença por RA (público)
curl http://localhost:8000/attendance/123456
```

No navegador (frontend), chame sempre com `credentials: "include"` nas rotas `/auth/...`, para o cookie do refresh ir e voltar.

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
- **O cookie do refresh não chega:** com `ORIGIN=*` ele não funciona entre origens. Liste a origem do frontend no `ORIGIN` e use `credentials: "include"`.
- **No Docker, a porta 8000 já está em uso:** feche o outro processo ou troque o lado esquerdo do `ports` no `compose.yml`.

## Estado atual e pendências

- Rotas, autenticação (access + refresh), rate limit, CORS, banco, comandos e testes estão prontos.
- **O logout só apaga o cookie.** O refresh token é um JWT sem registro no banco, então não dá para cancelá-lo no servidor: quem o copiou antes pode renová-lo até vencer (7 dias).
- **O `role` vai dentro do token.** Um admin rebaixado continua admin até o access token vencer (15 minutos).
- **Uma sessão de banco compartilhada.** A `ManageOperations` é uma só para todas as requisições, e a `AsyncSession` do SQLAlchemy não aceita uso simultâneo. Com muitas requisições ao mesmo tempo, o ideal é uma sessão por requisição.
- **O rate limit fica na memória do processo.** Com mais de um worker, cada um conta separado.
- **O `midlleware/routes.py` ainda não é usado pelo middleware:** o limite vale igual para todas as rotas.
