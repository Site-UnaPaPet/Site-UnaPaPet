"Chama /attendance/{ra} (consulta publica, sem token)"
from .client import Client


def run(client: Client, ctx: dict) -> None:

    client.call("GET", f"/attendance/{ctx['ra']}")
