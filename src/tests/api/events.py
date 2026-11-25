"Chama /events (publica) e /admin/events"
from .client import Client


def run(client: Client, ctx: dict) -> None:

    admin = ctx["admin"]
    event = admin.call("POST", "/admin/events", json={"title": "Feira", "starts_at": "2030-12-01T10:00:00", "location": "Campus"})
    ctx["event_id"] = event["id"]

    admin.call("GET", f"/admin/events/{event['id']}")
    admin.call("GET", "/admin/events")
    admin.call("PUT", f"/admin/events/{event['id']}", json={"title": "Feira Pet"})

    #públicas, sem token
    client.call("GET", "/events")
    client.call("GET", f"/events/{event['id']}")


def delete(client: Client, ctx: dict) -> None:

    ctx["admin"].call("DELETE", f"/admin/events/{ctx['event_id']}")
