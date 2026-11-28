"Junta todas as operações em uma única classe"
from sqlalchemy.ext.asyncio import AsyncSession
from .committees import CommitteesOperations
from .students import StudentsOperations
from .meetings import MeetingsOperations
from .attendances import AttendancesOperations
from .events import EventsOperations
from .posts import PostsOperations
from .forms import FormsOperations
from .users import UsersOperations


class ManageOperations(
    CommitteesOperations,
    StudentsOperations,
    MeetingsOperations,
    AttendancesOperations,
    EventsOperations,
    PostsOperations,
    FormsOperations,
    UsersOperations,
):

    def __init__(self, session: AsyncSession) -> None:

        #Passa a sessão para cada classe de operações
        for operations in ManageOperations.__bases__:
            operations.__init__(self, session)
