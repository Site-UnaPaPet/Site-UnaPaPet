"""Chama todas as rotas da API que está rodando em localhost: só faz as requisições, nada mais.

Acha os arquivos de teste desta pasta (menos este e o client.py) e roda o `run` de cada um, depois o `delete`
de cada um na ordem inversa. Qualquer status >= 400 levanta o erro e para.
Um arquivo novo nesta pasta entra sozinho: basta ter a função run(client, ctx) (e, se criar dados, delete(client, ctx)).

Não mexe no banco: o admin abaixo precisa JÁ EXISTIR na API que está sendo testada.
Roda da raiz do projeto:  python -m src.tests.api.main
"""
import importlib
from pathlib import Path

from src.tests.api.client import BASE_URL, Client

#Admin que já existe na API (usado para chamar as rotas /admin)
ADMIN = {"email": "admin@teste.com", "password": "admin1234"}

#Arquivos desta pasta que não são testes de rota
IGNORED = {"main", "client"}

#Os testes dependem uns dos outros (um usa o id que o outro criou), então estes rodam nessa ordem.
#Arquivos que não estão aqui rodam depois, em ordem alfabética.
ORDER = ["health", "auth", "admin", "committees", "students", "meetings", "attendances", "attendance", "events", "posts", "forms", "users"]


#Acha os arquivos de teste da pasta (menos o main e o client) e importa cada um
def find_tests() -> list:

    folder = Path(__file__).resolve().parent
    names = sorted(path.stem for path in folder.glob("*.py") if path.stem not in IGNORED and not path.stem.startswith("_"))

    names = [name for name in ORDER if name in names] + [name for name in names if name not in ORDER]
    modules = []

    for name in names:

        module = importlib.import_module(f"src.tests.api.{name}")

        if not hasattr(module, "run"):
            print(f"SKIP  {name}.py não tem run(client, ctx)")
            continue

        modules.append(module)

    return modules


def main() -> None:

    print(f"Chamando a API em {BASE_URL}")

    client = Client()
    ctx: dict = {"admin": Client().call("POST", "/auth/login", json=ADMIN)["access_token"]}
    modules = find_tests()

    #criar, ler e atualizar (a ordem importa: um usa o id do outro)
    for module in modules:
        module.run(client, ctx)

    #apagar o que foi criado (na ordem inversa: filhos antes dos pais)
    for module in reversed(modules):

        if hasattr(module, "delete"):
            module.delete(client, ctx)

    print("\nTodas as requisições passaram")


if __name__ == "__main__":
    main()
