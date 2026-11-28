"Chama /admin/committees"
from .client import RUN, Client


def run(client: Client, ctx: dict) -> None:

    admin = ctx["admin"]
    committee = admin.call("POST", "/admin/committees", json={"name": f"Eventos {RUN}"})
    ctx["committee_id"] = committee["id"]

    admin.call("GET", f"/admin/committees/{committee['id']}")
    admin.call("GET", "/admin/committees")
    admin.call("PUT", f"/admin/committees/{committee['id']}", json={"name": f"Eventos 2 {RUN}"})


def delete(client: Client, ctx: dict) -> None:

    ctx["admin"].call("DELETE", f"/admin/committees/{ctx['committee_id']}")
