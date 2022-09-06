from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from timetable_bot.config import DefaultSettings


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def refresh(self) -> None:
        self.engine = create_async_engine(DefaultSettings().database_uri, echo=True, future=True)


async def get_session() -> AsyncSession:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        return session


__all__ = [
    "get_session",
]
