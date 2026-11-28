"Chama /health"
from .client import Client


def run(client: Client, ctx: dict) -> None:

    client.call("GET", "/health")
