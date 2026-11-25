"Chama /admin/meetings"
from datetime import date, timedelta
from .client import RUN, Client


def run(client: Client, ctx: dict) -> None:

    admin = ctx["admin"]

    #datas únicas por rodada (a data da reunião não pode repetir)
    first_day = date(2030, 1, 1) + timedelta(days=int(RUN, 16) % 3000)
    dates = [first_day, first_day + timedelta(days=1), first_day + timedelta(days=2)]

    first = admin.call("POST", "/admin/meetings", json={"date": dates[0].isoformat()})
    second = admin.call("POST", "/admin/meetings", json={"date": dates[1].isoformat()})
    ctx["meeting_ids"] = [first["id"], second["id"]]

    admin.call("GET", f"/admin/meetings/{first['id']}")
    admin.call("GET", "/admin/meetings")
    admin.call("PUT", f"/admin/meetings/{second['id']}", json={"date": dates[2].isoformat()})


def delete(client: Client, ctx: dict) -> None:

    for meeting_id in ctx["meeting_ids"]:
        ctx["admin"].call("DELETE", f"/admin/meetings/{meeting_id}")
