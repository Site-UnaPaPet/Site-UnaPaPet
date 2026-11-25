"Chama /admin/attendances"
from .client import Client


def run(client: Client, ctx: dict) -> None:

    admin = ctx["admin"]
    first_meeting, second_meeting = ctx["meeting_ids"]

    present = admin.call("POST", "/admin/attendances", json={"student_id": ctx["student_id"], "meeting_id": first_meeting, "status": "PRESENT"})
    absent = admin.call("POST", "/admin/attendances", json={"student_id": ctx["student_id"], "meeting_id": second_meeting, "status": "ABSENT"})
    ctx["attendance_ids"] = [present["id"], absent["id"]]

    admin.call("GET", f"/admin/attendances/{present['id']}")
    admin.call("GET", "/admin/attendances")
    admin.call("GET", "/admin/attendances", student_id=ctx["student_id"])
    admin.call("GET", "/admin/attendances", meeting_id=first_meeting)
    admin.call("PUT", f"/admin/attendances/{absent['id']}", json={"status": "EXCUSED"})


def delete(client: Client, ctx: dict) -> None:

    for attendance_id in ctx["attendance_ids"]:
        ctx["admin"].call("DELETE", f"/admin/attendances/{attendance_id}")
