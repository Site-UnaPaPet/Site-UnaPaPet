"Chama /posts (publica) e /admin/posts"
from .client import Client


def run(client: Client, ctx: dict) -> None:

    token = ctx["admin"]
    post = client.call("POST", "/admin/posts", json={"title": "Novidade", "published_at": "2030-11-01T10:00:00", "summary": "resumo"}, token=token)
    ctx["post_id"] = post["id"]

    client.call("GET", f"/admin/posts/{post['id']}", token=token)
    client.call("GET", "/admin/posts", token=token)
    client.call("PUT", f"/admin/posts/{post['id']}", json={"title": "Novidade 2"}, token=token)

    #públicas, sem token
    client.call("GET", "/posts")
    client.call("GET", f"/posts/{post['id']}")


def delete(client: Client, ctx: dict) -> None:

    client.call("DELETE", f"/admin/posts/{ctx['post_id']}", token=ctx["admin"])
