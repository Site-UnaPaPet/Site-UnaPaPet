"Chama /admin/students"
from .client import RUN, Client


def run(client: Client, ctx: dict) -> None:

    token = ctx["admin"]
    student = client.call("POST", "/admin/students", json={"ra": f"{RUN}-1", "name": "Ana", "committee_id": ctx["committee_id"]}, token=token)
    inactive = client.call("POST", "/admin/students", json={"ra": f"{RUN}-2", "name": "Inativo", "committee_id": ctx["committee_id"], "active": False}, token=token)
    ctx["student_id"], ctx["ra"] = student["id"], student["ra"]
    ctx["inactive_id"], ctx["inactive_ra"] = inactive["id"], inactive["ra"]

    client.call("GET", f"/admin/students/{student['id']}", token=token)
    client.call("GET", "/admin/students", token=token)
    client.call("GET", "/admin/students", token=token, only_active="true")
    client.call("GET", "/admin/students", token=token, committee_id=ctx["committee_id"])
    client.call("PUT", f"/admin/students/{student['id']}", json={"name": "Ana B"}, token=token)


def delete(client: Client, ctx: dict) -> None:

    client.call("DELETE", f"/admin/students/{ctx['student_id']}", token=ctx["admin"])
    client.call("DELETE", f"/admin/students/{ctx['inactive_id']}", token=ctx["admin"])
