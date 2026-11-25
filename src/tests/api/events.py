"Chama /events (publica) e /admin/events"
from .client import Client


def run(client: Client, ctx: dict) -> None:

    token = ctx["admin"]
    event = client.call("POST", "/admin/events", json={"title": "Feira", "starts_at": "2030-12-01T10:00:00", "location": "Campus"}, token=token)
    ctx["event_id"] = event["id"]

    client.call("GET", f"/admin/events/{event['id']}", token=token)
    client.call("GET", "/admin/events", token=token)
    client.call("PUT", f"/admin/events/{event['id']}", json={"title": "Feira Pet"}, token=token)

    #públicas, sem token
    client.call("GET", "/events")
    client.call("GET", f"/events/{event['id']}")


def delete(client: Client, ctx: dict) -> None:

    client.call("DELETE", f"/admin/events/{ctx['event_id']}", token=ctx["admin"])
