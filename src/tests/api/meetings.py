"Chama /admin/meetings"
from datetime import date, timedelta
from .client import RUN, Client


def run(client: Client, ctx: dict) -> None:

    token = ctx["admin"]

    #datas únicas por rodada (a data da reunião não pode repetir)
    first_day = date(2030, 1, 1) + timedelta(days=int(RUN, 16) % 3000)
    dates = [first_day, first_day + timedelta(days=1), first_day + timedelta(days=2)]

    first = client.call("POST", "/admin/meetings", json={"date": dates[0].isoformat()}, token=token)
    second = client.call("POST", "/admin/meetings", json={"date": dates[1].isoformat()}, token=token)
    ctx["meeting_ids"] = [first["id"], second["id"]]

    client.call("GET", f"/admin/meetings/{first['id']}", token=token)
    client.call("GET", "/admin/meetings", token=token)
    client.call("PUT", f"/admin/meetings/{second['id']}", json={"date": dates[2].isoformat()}, token=token)


def delete(client: Client, ctx: dict) -> None:

    for meeting_id in ctx["meeting_ids"]:
        client.call("DELETE", f"/admin/meetings/{meeting_id}", token=ctx["admin"])
