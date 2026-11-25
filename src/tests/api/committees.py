"Chama /admin/committees"
from .client import RUN, Client


def run(client: Client, ctx: dict) -> None:

    token = ctx["admin"]
    committee = client.call("POST", "/admin/committees", json={"name": f"Eventos {RUN}"}, token=token)
    ctx["committee_id"] = committee["id"]

    client.call("GET", f"/admin/committees/{committee['id']}", token=token)
    client.call("GET", "/admin/committees", token=token)
    client.call("PUT", f"/admin/committees/{committee['id']}", json={"name": f"Eventos 2 {RUN}"}, token=token)


def delete(client: Client, ctx: dict) -> None:

    client.call("DELETE", f"/admin/committees/{ctx['committee_id']}", token=ctx["admin"])
