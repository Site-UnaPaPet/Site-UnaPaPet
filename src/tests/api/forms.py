"Chama /forms (publica) e /admin/forms"
from .client import Client


def run(client: Client, ctx: dict) -> None:

    admin = ctx["admin"]
    active = admin.call("POST", "/admin/forms", json={"title": "Ativo", "url": "https://exemplo.com/a", "position": 2})
    hidden = admin.call("POST", "/admin/forms", json={"title": "Escondido", "url": "https://exemplo.com/b", "active": False})
    ctx["form_ids"] = [active["id"], hidden["id"]]

    admin.call("GET", f"/admin/forms/{active['id']}")
    admin.call("GET", "/admin/forms")
    admin.call("PUT", f"/admin/forms/{active['id']}", json={"position": 1})

    #pública, sem token
    client.call("GET", "/forms")


def delete(client: Client, ctx: dict) -> None:

    for form_id in ctx["form_ids"]:
        ctx["admin"].call("DELETE", f"/admin/forms/{form_id}")
