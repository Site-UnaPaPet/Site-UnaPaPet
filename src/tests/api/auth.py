"Chama /auth (register, login, refresh e logout)"
from .client import RUN, Client


def run(client: Client, ctx: dict) -> None:

    member = {"email": f"membro-{RUN}@teste.com", "password": "senha1234"}

    client.call("POST", "/auth/register", json=member)
    client.call("POST", "/auth/login", json=member)
    client.call("POST", "/auth/refresh")
    client.call("POST", "/auth/logout")
