# Frontend — UnaPáPet

![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![React Router](https://img.shields.io/badge/React_Router-7-CA4245?style=for-the-badge&logo=reactrouter&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-22-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![npm](https://img.shields.io/badge/npm-CB3837?style=for-the-badge&logo=npm&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

Frontend do site do UnaPáPet, feito em **React + TypeScript** (com Vite). Todo o código fica em `src/frontend/`.

O design de referência está em `docs/template.zip` (6 telas mobile e a paleta de cores).

## Estrutura de pastas

```
Site-UnaPaPet/
├── .env.example              ← na raiz do projeto, antes de src/
├── docs/
└── src/
    └── frontend/
        ├── index.html
        ├── package.json, tsconfig.json, vite.config.ts
        ├── main.tsx
        ├── App.tsx
        ├── routes/
        │   └── AppRoutes.tsx
        ├── services/
        │   ├── api.ts            ← cliente HTTP genérico (request, ApiError, criarCrud)
        │   ├── auth.ts           ← cadastro, login, refresh, logout
        │   ├── eventos.ts, posts.ts, formularios.ts
        │   ├── presenca.ts       ← consulta pública por RA
        │   └── comissoes.ts, alunos.ts, reunioes.ts, presencas.ts, usuarios.ts   ← só admin
        ├── pages/
        │   ├── Home/Home.tsx
        │   ├── Calendario/Calendario.tsx
        │   ├── Formularios/Formularios.tsx
        │   ├── Presenca/Presenca.tsx
        │   ├── Presenca/ConsultaRA.tsx
        │   └── Blog/Blog.tsx
        ├── components/
        │   └── layout/
        │       ├── Layout.tsx
        │       ├── Header.tsx
        │       ├── Footer.tsx
        │       └── PageBanner.tsx
        ├── styles/
        │   ├── variables.css
        │   ├── global.css
        │   ├── components.css
        │   └── pages/
        │       ├── home.css
        │       ├── calendario.css
        │       ├── formularios.css
        │       ├── presenca.css
        │       └── blog.css
        └── assets/
```

## Como as peças se conectam

```
index.html → main.tsx → App.tsx → Layout (Header + conteúdo + Footer)
                                      └── AppRoutes → pages/* → services/* → backend
```

1. O navegador abre o `index.html`, que carrega o `main.tsx`.
2. O `main.tsx` monta o `App` e importa os CSS globais.
3. O `App` coloca as rotas dentro do `Layout`.
4. O `AppRoutes` escolhe a página pela URL.
5. A página busca dados no backend **somente** através do `services/`.

## O que cada arquivo deve ter

### Na raiz do projeto

| Arquivo | O que deve ter | Para que serve |
|---|---|---|
| `.env.example` | Uma linha por variável de ambiente, com valor de exemplo e um comentário. Hoje: `VITE_API_URL` (URL do backend). Nunca coloque segredos reais. | Modelo para o time. Cada pessoa copia para `.env` (que não vai para o git) e ajusta os valores. Toda variável lida pelo frontend precisa começar com `VITE_`. |

> O `.env` fica na raiz do projeto, e não em `src/frontend/`. Por isso o `vite.config.ts` precisa apontar para lá (`envDir`). Isso será configurado no setup do Vite.

### `src/frontend/` (arquivos soltos)

| Arquivo | O que deve ter | Para que serve |
|---|---|---|
| `index.html` | A `<div id="root">`, o `<script type="module" src="/main.tsx">`, o `<title>`, as meta tags (`lang="pt-BR"`, viewport, descrição), o favicon e o carregamento das fontes. **Nenhum conteúdo de página.** | É a única página HTML real do site. O React desenha tudo dentro da `#root`. |
| `main.tsx` | A chamada `createRoot(...).render(...)`, o `BrowserRouter` envolvendo o `<App />` e os imports dos CSS globais (`variables.css`, `global.css`, `components.css`), nessa ordem. | Ponto de entrada. Liga o React ao HTML e carrega os estilos que valem para o site todo. Não tem lógica de negócio. |
| `App.tsx` | O `<Layout>` envolvendo o `<AppRoutes />`. | Componente raiz. Junta a estrutura da tela com as rotas. Deve ficar pequeno. |

### `routes/`

| Arquivo | O que deve ter | Para que serve |
|---|---|---|
| `AppRoutes.tsx` | Um `<Routes>` com uma `<Route>` por página: `/` (Home), `/calendario`, `/formularios`, `/presenca`, `/presenca/consulta` e `/blog`. Opcionalmente uma rota `*` para página não encontrada. | É o mapa de URLs do site. Toda página nova precisa de uma rota aqui, senão não abre. |

### `services/`

É o **único** lugar que conversa com o backend. Cada arquivo tem os tipos TypeScript das respostas e as funções de um assunto. Os nomes dos campos são os mesmos da API (`starts_at`, `image_url`...). A referência completa das rotas está em `docs/backend.md`.

| Arquivo | O que tem |
|---|---|
| `api.ts` | `request<T>(método, caminho, opções)`: a função genérica. Lê `VITE_API_URL`, manda `credentials: "include"` em toda chamada, converte a resposta em JSON (e o `204` em `undefined`) e levanta `ApiError` quando o status é >= 400. Também `criarCrud(base)`, que gera as 5 rotas de admin de um recurso. |
| `auth.ts` | `registrar`, `entrar`, `renovar`, `sair`, `buscarAdmin` e `souAdmin` (devolve `true`/`false`; serve para decidir se mostra o painel). |
| `eventos.ts` | `listarEventos`, `buscarEvento` (públicas) e `eventosAdmin`. |
| `posts.ts` | `listarPosts`, `buscarPost` (públicas) e `postsAdmin`. |
| `formularios.ts` | `listarFormularios` (pública, só os ativos) e `formulariosAdmin`. |
| `presenca.ts` | `consultarPresenca(ra)`: consulta pública por RA. |
| `comissoes.ts`, `alunos.ts`, `reunioes.ts`, `presencas.ts`, `usuarios.ts` | Só admin: `comissoesAdmin`, `alunosAdmin` (+ `listarAlunos` com filtros), `reunioesAdmin`, `presencasAdmin` (+ `listarPresencas` com filtros) e `usuariosAdmin`. |

Os `...Admin` têm as funções `listar(query?)`, `buscar(id)`, `criar(dados)`, `atualizar(id, dados)` e `apagar(id)`.

**Como usar numa página:**

```tsx
import { useEffect, useState } from "react";
import { listarEventos, type Evento } from "../../services/eventos";
import { ApiError } from "../../services/api";

const [eventos, setEventos] = useState<Evento[] | null>(null);   // null = carregando
const [erro, setErro] = useState("");

useEffect(() => {
  listarEventos()
    .then(setEventos)
    .catch((e: unknown) => setErro(e instanceof ApiError ? e.message : "Erro inesperado."));
}, []);
```

**Login:** o backend guarda o token em cookies `httpOnly`, então **não existe token no JavaScript** (nada de `localStorage`). Depois de `entrar(...)`, todas as chamadas já vão autenticadas. Se o login vencer (15 minutos), o `request` renova sozinho (`/auth/refresh`) e repete a chamada, uma vez. Várias chamadas ao mesmo tempo compartilham a mesma renovação.

**Erros:** toda falha vira `ApiError`, com `status` (`0` = sem conexão), `detail` (texto técnico do backend) e `message` (texto em português, pronto para mostrar na tela, como "E-mail ou senha incorretos." ou "Este e-mail já está cadastrado.").

**Para funcionar no navegador:** a variável `ORIGIN` do backend precisa ter a URL do site (`http://localhost:5173`). Com `ORIGIN=*` o navegador não envia os cookies e o login não funciona.

O que cada página usa:

| Página | Função |
|---|---|
| Home e Blog | `listarPosts()` |
| Calendário | `listarEventos()` |
| Formulários | `listarFormularios()` |
| Consulta por RA | `consultarPresenca(ra)` |

### `pages/`

Cada pasta é uma página. A página monta a tela, busca os dados (via `services/`) e importa o CSS correspondente de `styles/pages/`. Cada página usa o `PageBanner` no topo, exceto a Home.

| Arquivo | Tela | O que deve ter |
|---|---|---|
| `Home/Home.tsx` | Início | Hero com a frase "Cuidando hoje, por um amanhã melhor!", imagem e botão "Conheça nosso projeto". Quatro cards de atalho (Calendário, Lista de presença, Formulários, Blog), cada um levando à sua rota. Seção "Últimas postagens" com 2 cards de post e o link "Ver todas". |
| `Calendario/Calendario.tsx` | Calendário | Banner. Calendário mensal com setas para mudar o mês e o nome do mês/ano. Seção "Próximos Eventos" com cartões (miniatura, título, local e horário). O estado do mês exibido fica aqui. |
| `Formularios/Formularios.tsx` | Formulários | Banner. Imagem de destaque. Lista de formulários, cada linha com o nome e o botão "Acessar" que abre o link. |
| `Presenca/Presenca.tsx` | Presença | Banner. Título "Subcomissões" e um botão por subcomissão: Triagem Clínica, Manejo sanitário, Clínica e cirurgia, Acolhimento e adoção, Banco de dados, Comunicação, Conforto e bem-estar animal. |
| `Presenca/ConsultaRA.tsx` | Consulta por RA | Banner. Campo de busca, botão "Buscar", e a área do resultado com estados de carregando, vazio e erro. O RA digitado fica no estado da página. |
| `Blog/Blog.tsx` | Blog | Banner. Galeria de fotos e o botão/link do Instagram da equipe. |

### `components/layout/`

Peças que se repetem em todas as páginas. Só entram aqui componentes de estrutura compartilhada.

| Arquivo | O que deve ter | Para que serve |
|---|---|---|
| `Layout.tsx` | `<Header />`, a área do conteúdo (`children`) e `<Footer />`. | Moldura única de todas as telas, para não repetir cabeçalho e rodapé em cada página. |
| `Header.tsx` | Logo (que leva à Home) e o menu: Início, Calendário, Formulários, Presença, Blog. Usa `NavLink` para marcar o item da página ativa. | Navegação do site. O item ativo aparece na pílula rosada, como no design. |
| `Footer.tsx` | Logo, ícone/link de contato por e-mail e a patinha decorativa. | Rodapé presente em todas as páginas. |
| `PageBanner.tsx` | Props `titulo`, `subtitulo` e `icone` (tipadas). Renderiza a faixa bege ondulada com as patinhas. | Cabeçalho visual das páginas internas, no mesmo padrão em todas. |

### `styles/`

| Arquivo | O que deve ter | Para que serve |
|---|---|---|
| `variables.css` | Só o bloco `:root` com variáveis: cores da paleta, famílias de fonte, tamanhos, espaçamentos e raios de borda. | Fonte única das cores e medidas. Trocar uma cor aqui muda o site todo. Não tem regras de seletor. |
| `global.css` | Reset básico (`box-sizing`, margens), estilos do `body` (fundo, cor do texto, fonte), tipografia base, links e imagens. | Estilo base que vale para o site inteiro. Usa as variáveis de `variables.css`. |
| `components.css` | Estilos de `Header`, `Footer`, `PageBanner` e dos elementos compartilhados (botões, cards). | Estilo de tudo que aparece em mais de uma página. |
| `pages/*.css` | Um arquivo por página, só com as regras daquela tela. Use classes com prefixo da página (ex.: `.home-hero`, `.calendario-grid`). | Evita que o estilo de uma página afete as outras. |

### `assets/`

Imagens (fotos, logo), ícones e fontes usados no site. Importe os arquivos nos componentes, em vez de usar caminhos soltos. Use nomes em minúsculo e sem espaços (`logo-unapapet.svg`), e prefira SVG para ícones e `.webp` para fotos, para o site carregar rápido.

## Paleta de cores

Valores aproximados tirados do template, que devem ser confirmados com o time de design e ficar em `variables.css`.

| Cor | Valor |
|---|---|
| Marrom escuro | `#552E2E` |
| Vermelho | `#A80000` |
| Preto | `#1E1E1E` |
| Off-white (fundo) | `#F5F3EF` |
| Creme | `#EFE2D3` |
| Bege | `#DEBA9B` |

## Regras

### Estrutura
- **Não crie pastas nem arquivos fora desta estrutura sem combinar com o time.** A ideia é manter o projeto pequeno e fácil de achar as coisas.
- **Nova página:** crie `pages/Nome/Nome.tsx`, o CSS em `styles/pages/nome.css` e a rota em `AppRoutes.tsx`. Se for um item do menu, adicione também no `Header.tsx`.
- **Novo componente:** se for usado em mais de uma página, crie em `components/`. Se for de uma página só, deixe dentro do arquivo da própria página.
- **Cada página mexe só nos seus arquivos.** Evite editar a página de outra pessoa; se precisar mudar algo compartilhado (`Layout`, `Header`, `components.css`), avise o time.

### Código
- **Nomes:** componentes e páginas em `PascalCase.tsx`, serviços em `camelCase.ts`, CSS em `minusculo.css`. Uma página/componente por arquivo, e o nome do arquivo igual ao nome do componente.
- **Componentes de função** com `export default`, sem classes.
- **TypeScript:** tipe as props dos componentes e as respostas da API. Não use `any`. Um tipo usado em vários arquivos fica junto do serviço que o devolve.
- **Sem lógica pesada no JSX:** se uma conta ou transformação ficar grande, extraia para uma função acima do `return`.
- **Textos em português** e sem texto "solto" repetido em vários arquivos.

### Backend
- **Nunca chame `fetch` (ou axios) direto numa página ou componente.** Sempre use uma função de `services/`.
- **A URL do backend não pode estar escrita no código.** Use `VITE_API_URL`, vinda do `.env`.
- **Toda chamada precisa tratar os 3 estados:** carregando, erro e sem dados. A tela nunca pode ficar em branco ou quebrar.
- **Dados de alunos (como a presença por RA) são sensíveis.** Não coloque esses dados em `console.log`, nem em URLs, nem no código.

### Estilo
- **Cores, fontes e medidas vêm sempre de `variables.css`.** Não escreva `#552E2E` direto em outro arquivo.
- **Mobile primeiro:** o design é mobile; escreva o CSS base para celular e use `@media (min-width: ...)` para telas maiores.
- **CSS de página fica no arquivo da página**, com classes prefixadas pelo nome da página, para não vazar para as outras.

### Git
- Trabalhe em branch própria (ex.: `feature/pagina-calendario`) e abra PR para `main`.
- Commits pequenos e com mensagem clara (`feat:`, `fix:`, `style:`).
- **Nunca commite o `.env`**, só o `.env.example`.

## Como rodar

Em qualquer uma das formas, o primeiro passo é o mesmo: na **raiz do projeto**, copie o `.env.example` para `.env` e ajuste o `VITE_API_URL` para o endereço do backend.

```bash
cp .env.example .env
```

Depois, o site abre em **http://localhost:5173**.

### Forma 1: npm puro (sem Docker)

Precisa ter o Node.js instalado (versão 22 ou mais nova).

```bash
cd src/frontend
npm install        # só na primeira vez, ou quando mudar o package.json
npm run dev        # servidor de desenvolvimento, atualiza ao salvar
```

Outros comandos úteis:

```bash
npm run build      # confere os tipos e gera a versão de produção (pasta dist/)
npm run preview    # abre a versão gerada pelo build
```

Para parar, `Ctrl + C`.

### Forma 2: só com o Dockerfile (`Dockerfile.interface`)

Precisa ter o Docker instalado. Rode tudo **na raiz do projeto**, e não dentro de `src/frontend`.

```bash
# 1. Construir a imagem (refaça quando mudar o código ou o package.json)
docker build -f Dockerfile.interface -t unapapet-frontend .

# 2. Subir o container
docker run --rm -p 5173:5173 -e VITE_API_URL=http://localhost:3000 unapapet-frontend
```

- O `.env` não entra na imagem, então a URL do backend vai pelo `-e VITE_API_URL=...`.
- Se a porta 5173 já estiver em uso, troque o lado esquerdo, por exemplo `-p 5199:5173`, e abra `http://localhost:5199`.
- Esta forma não atualiza ao salvar: depois de mudar o código, é preciso refazer o build e subir de novo.
- Para parar, `Ctrl + C`.

### Forma 3: Docker Compose (`compose.yml`)

Precisa ter o Docker com o Compose. É a forma mais prática, porque já lê o `.env` da raiz sozinha e vai servir também para subir o backend junto no futuro.

```bash
docker compose up --build      # constrói e sobe (veja os logs no terminal)
docker compose up -d           # sobe em segundo plano
docker compose logs -f         # acompanha os logs
docker compose down            # para e remove o container
```

- O serviço do frontend se chama `interface` e recebe o `VITE_API_URL` do `.env`.
- Depois de mudar o `.env`, recrie o container: `docker compose up -d --force-recreate`.
- Depois de mudar o código ou o `package.json`, use `docker compose up --build`.
- Para o site abrir no navegador, o serviço precisa publicar a porta: o `compose.yml` deve ter `ports: - "5173:5173"` no serviço `interface`.

### Qual usar?

| Forma | Quando usar |
|---|---|
| npm puro | No dia a dia do frontend: é a mais rápida e atualiza ao salvar. |
| Dockerfile | Para testar se a imagem do frontend funciona isolada. |
| Compose | Para subir o projeto completo do mesmo jeito em qualquer máquina. |

### Problemas comuns

- **`address already in use` / porta ocupada:** já tem algo na porta 5173 (talvez um `npm run dev` aberto). Feche o outro ou troque a porta.
- **`VITE_API_URL` vazio ou `undefined`:** o `.env` não existe na raiz, ou a variável não começa com `VITE_`.
- **O navegador não consegue chamar o backend:** o `VITE_API_URL` roda no navegador, então precisa ser um endereço que ele alcança (`http://localhost:3000`), e não o nome de um serviço do Compose.
- **Tela em branco:** é o esperado enquanto as páginas ainda são esqueletos sem conteúdo.

## Estado atual

- O projeto já roda (`npm run dev` abre uma página em branco). O setup está pronto: `package.json`, `tsconfig.json`, `vite.config.ts` (com `envDir` apontando para a raiz) e o `.gitignore` na raiz.
- `index.html` e `main.tsx` já têm o mínimo para iniciar o app.
- Os `services/` estão prontos (funções, tipos e tratamento de erro) e conferidos com `tsc --noEmit` e contra a API de verdade. Falta ligar as páginas a eles.
- Os demais `.tsx` são só esqueletos, sem conteúdo. Os `.css` estão vazios.
