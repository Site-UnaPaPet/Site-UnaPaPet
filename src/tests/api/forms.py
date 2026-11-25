"Chama /forms (publica) e /admin/forms"
from .client import Client


def run(client: Client, ctx: dict) -> None:

    token = ctx["admin"]
    active = client.call("POST", "/admin/forms", json={"title": "Ativo", "url": "https://exemplo.com/a", "position": 2}, token=token)
    hidden = client.call("POST", "/admin/forms", json={"title": "Escondido", "url": "https://exemplo.com/b", "active": False}, token=token)
    ctx["form_ids"] = [active["id"], hidden["id"]]

    client.call("GET", f"/admin/forms/{active['id']}", token=token)
    client.call("GET", "/admin/forms", token=token)
    client.call("PUT", f"/admin/forms/{active['id']}", json={"position": 1}, token=token)

    #pública, sem token
    client.call("GET", "/forms")


def delete(client: Client, ctx: dict) -> None:

    for form_id in ctx["form_ids"]:
        client.call("DELETE", f"/admin/forms/{form_id}", token=ctx["admin"])
