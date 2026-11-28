"Chama /posts (publica) e /admin/posts"
from .client import Client


def run(client: Client, ctx: dict) -> None:

    admin = ctx["admin"]
    post = admin.call("POST", "/admin/posts", json={"title": "Novidade", "published_at": "2030-11-01T10:00:00", "summary": "resumo"})
    ctx["post_id"] = post["id"]

    admin.call("GET", f"/admin/posts/{post['id']}")
    admin.call("GET", "/admin/posts")
    admin.call("PUT", f"/admin/posts/{post['id']}", json={"title": "Novidade 2"})

    #públicas, sem token
    client.call("GET", "/posts")
    client.call("GET", f"/posts/{post['id']}")


def delete(client: Client, ctx: dict) -> None:

    ctx["admin"].call("DELETE", f"/admin/posts/{ctx['post_id']}")
