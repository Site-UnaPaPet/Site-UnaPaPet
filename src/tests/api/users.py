"Chama /admin/users"
from .client import RUN, Client


def run(client: Client, ctx: dict) -> None:

    token = ctx["admin"]
    email = f"novo-{RUN}@teste.com"
    user = client.call("POST", "/admin/users", json={"email": email, "password": "novasenha1", "role": "member"}, token=token)
    ctx["user_id"] = user["id"]

    client.call("GET", f"/admin/users/{user['id']}", token=token)
    client.call("GET", "/admin/users", token=token)
    client.call("PUT", f"/admin/users/{user['id']}", json={"role": "admin"}, token=token)
    client.call("PUT", f"/admin/users/{user['id']}", json={"password": "outrasenha1"}, token=token)
    client.call("POST", "/auth/login", json={"email": email, "password": "outrasenha1"})


def delete(client: Client, ctx: dict) -> None:

    client.call("DELETE", f"/admin/users/{ctx['user_id']}", token=ctx["admin"])
