"Chama /admin (com o cookie e com o cabecalho Authorization)"
from .client import Client


def run(client: Client, ctx: dict) -> None:

    #1. só com o cookie access_token (o admin fez login, então o Client já tem o cookie)
    ctx["admin"].call("GET", "/admin")

    #2. alternativa sem cookie: o access_token vem no corpo do login e vai no cabeçalho (cliente novo, sem cookies)
    Client().call("GET", "/admin", token=ctx["token"])
