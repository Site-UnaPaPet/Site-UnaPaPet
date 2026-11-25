"Chama /admin/users"
from .client import RUN, Client


def run(client: Client, ctx: dict) -> None:

    admin = ctx["admin"]
    email = f"novo-{RUN}@teste.com"
    user = admin.call("POST", "/admin/users", json={"email": email, "password": "novasenha1", "role": "member"})
    ctx["user_id"] = user["id"]

    admin.call("GET", f"/admin/users/{user['id']}")
    admin.call("GET", "/admin/users")
    admin.call("PUT", f"/admin/users/{user['id']}", json={"role": "admin"})
    admin.call("PUT", f"/admin/users/{user['id']}", json={"password": "outrasenha1"})
    client.call("POST", "/auth/login", json={"email": email, "password": "outrasenha1"})


def delete(client: Client, ctx: dict) -> None:

    ctx["admin"].call("DELETE", f"/admin/users/{ctx['user_id']}")
