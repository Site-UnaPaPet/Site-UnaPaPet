"""Teste do banco de dados: cria as tabelas, testa todas as operations em ordem e depois apaga tudo.

Roda da raiz do projeto:  python -m src.tests.db
Usa o banco configurado em URL_DB (.env ou variável de ambiente) e apaga as tabelas no final,
então aponte só para um banco de teste.
"""
import asyncio
import datetime

from src.backend.database.manage import ManageDb
from src.backend.database.models import AttendanceStatus
from src.backend.exceptions import DatabaseOperationError
from src.backend.logs import logger


async def run_operations(ops) -> None:

    #committees
    committee = await ops.create_committee("Eventos")
    assert committee.id is not None
    assert (await ops.get_committee(committee.id)).name == "Eventos"
    assert (await ops.get_committee_by_name("Eventos")).id == committee.id
    assert len(await ops.list_committees()) == 1
    assert (await ops.update_committee(committee.id, "Eventos 2")).name == "Eventos 2"
    assert await ops.update_committee(999, "x") is None

    #students
    student = await ops.create_student("123456", "Ana", committee.id)
    assert (await ops.get_student(student.id)).ra == "123456"
    assert (await ops.get_student_by_ra("123456")).id == student.id
    assert await ops.get_student_by_ra("000") is None
    bia = await ops.create_student("654321", "Bia", committee.id, active=False)
    assert len(await ops.list_students()) == 2
    assert len(await ops.list_students(only_active=True)) == 1
    assert len(await ops.list_students(committee_id=committee.id)) == 2
    assert (await ops.update_student(student.id, name="Ana B")).name == "Ana B"
    assert await ops.update_student(999, name="x") is None

    #meetings
    today = datetime.date.today()
    meeting = await ops.create_meeting(today)
    other = await ops.create_meeting(today + datetime.timedelta(days=7))
    assert (await ops.get_meeting(meeting.id)).date == today
    assert (await ops.get_meeting_by_date(today)).id == meeting.id
    assert len(await ops.list_meetings()) == 2
    new_date = today + datetime.timedelta(days=14)
    assert (await ops.update_meeting(other.id, new_date)).date == new_date

    #attendances
    attendance = await ops.create_attendance(student.id, meeting.id, AttendanceStatus.PRESENT)
    assert (await ops.get_attendance(attendance.id)).status == AttendanceStatus.PRESENT
    assert (await ops.get_attendance_by_student_meeting(student.id, meeting.id)).id == attendance.id
    assert len(await ops.list_attendances_by_student(student.id)) == 1
    assert len(await ops.list_attendances_by_meeting(meeting.id)) == 1
    assert (await ops.count_attendances_by_status(student.id))[AttendanceStatus.PRESENT] == 1
    assert (await ops.update_attendance_status(attendance.id, AttendanceStatus.EXCUSED)).status == AttendanceStatus.EXCUSED

    #o rollback de uma operação com erro expira os objetos já carregados, então guarda os ids antes
    student_id, meeting_id, attendance_id, bia_id, committee_id = student.id, meeting.id, attendance.id, bia.id, committee.id

    #erros do banco viram DatabaseOperationError (RA e presença duplicados)
    for call in (
        ops.create_student("123456", "Duplicado", committee_id),
        ops.create_attendance(student_id, meeting_id, AttendanceStatus.ABSENT),
    ):
        try:
            await call
            raise AssertionError("deveria ter levantado DatabaseOperationError")
        except DatabaseOperationError:
            pass

    #events
    event = await ops.create_event("Feira", datetime.datetime.now(), location="Campus")
    assert (await ops.get_event(event.id)).title == "Feira"
    assert len(await ops.list_events()) == 1
    assert (await ops.update_event(event.id, title="Feira Pet")).title == "Feira Pet"

    #posts
    post = await ops.create_post("Novidade", datetime.datetime.now(), summary="resumo")
    assert (await ops.get_post(post.id)).title == "Novidade"
    assert len(await ops.list_posts()) == 1
    assert (await ops.update_post(post.id, title="Novidade 2")).title == "Novidade 2"

    #forms
    form = await ops.create_form("Inscrição", "https://exemplo.com", position=1)
    assert (await ops.get_form(form.id)).url == "https://exemplo.com"
    assert len(await ops.list_forms()) == 1
    assert (await ops.update_form(form.id, active=False)).active is False

    #users
    user = await ops.create_user("admin@exemplo.com", "hash")
    assert (await ops.get_user(user.id)).email == "admin@exemplo.com"
    assert len(await ops.list_users()) == 1
    assert (await ops.update_user(user.id, role="editor")).role == "editor"

    #deletes (filhos antes dos pais)
    assert await ops.delete_attendance(attendance_id)
    assert not await ops.delete_attendance(attendance_id)
    assert await ops.delete_student(student_id)
    assert await ops.delete_meeting(meeting_id)
    assert await ops.delete_student(bia_id)
    assert await ops.delete_committee(committee_id)
    assert not await ops.delete_committee(committee_id)
    assert await ops.delete_event(event.id)
    assert await ops.delete_post(post.id)
    assert await ops.delete_form(form.id)
    assert await ops.delete_user(user.id)


async def main() -> None:

    db = ManageDb()

    #1. cria as tabelas (se não existirem)
    migrate = await db.migrate()
    migrate.create_tables()

    #2. testa todas as operations
    try:

        ops = await db.operations()
        try:
            await run_operations(ops)
        finally:
            await ops.session.close()
        logger.success("TODOS OS TESTES PASSARAM")

    #3. apaga o banco com o migrate, mesmo se o teste falhar
    finally:

        migrate = await db.migrate()
        migrate.drop_tables()


if __name__ == "__main__":
    asyncio.run(main())
