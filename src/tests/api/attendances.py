"Chama /admin/attendances"
from .client import Client


def run(client: Client, ctx: dict) -> None:

    token = ctx["admin"]
    first_meeting, second_meeting = ctx["meeting_ids"]

    present = client.call("POST", "/admin/attendances", json={"student_id": ctx["student_id"], "meeting_id": first_meeting, "status": "PRESENT"}, token=token)
    absent = client.call("POST", "/admin/attendances", json={"student_id": ctx["student_id"], "meeting_id": second_meeting, "status": "ABSENT"}, token=token)
    ctx["attendance_ids"] = [present["id"], absent["id"]]

    client.call("GET", f"/admin/attendances/{present['id']}", token=token)
    client.call("GET", "/admin/attendances", token=token)
    client.call("GET", "/admin/attendances", token=token, student_id=ctx["student_id"])
    client.call("GET", "/admin/attendances", token=token, meeting_id=first_meeting)
    client.call("PUT", f"/admin/attendances/{absent['id']}", json={"status": "EXCUSED"}, token=token)


def delete(client: Client, ctx: dict) -> None:

    for attendance_id in ctx["attendance_ids"]:
        client.call("DELETE", f"/admin/attendances/{attendance_id}", token=ctx["admin"])
