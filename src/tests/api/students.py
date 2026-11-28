"Chama /admin/students"
from .client import RUN, Client


def run(client: Client, ctx: dict) -> None:

    admin = ctx["admin"]
    student = admin.call("POST", "/admin/students", json={"ra": f"{RUN}-1", "name": "Ana", "committee_id": ctx["committee_id"]})
    inactive = admin.call("POST", "/admin/students", json={"ra": f"{RUN}-2", "name": "Inativo", "committee_id": ctx["committee_id"], "active": False})
    ctx["student_id"], ctx["ra"] = student["id"], student["ra"]
    ctx["inactive_id"], ctx["inactive_ra"] = inactive["id"], inactive["ra"]

    admin.call("GET", f"/admin/students/{student['id']}")
    admin.call("GET", "/admin/students")
    admin.call("GET", "/admin/students", only_active="true")
    admin.call("GET", "/admin/students", committee_id=ctx["committee_id"])
    admin.call("PUT", f"/admin/students/{student['id']}", json={"name": "Ana B"})


def delete(client: Client, ctx: dict) -> None:

    ctx["admin"].call("DELETE", f"/admin/students/{ctx['student_id']}")
    ctx["admin"].call("DELETE", f"/admin/students/{ctx['inactive_id']}")
