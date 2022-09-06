from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID, TEXT, INTEGER
from sqlalchemy.sql import func

from timetable_bot.db import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique index of element (type UUID)",
    )
    dt_created = Column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
        doc="Date and time of creation (type TIMESTAMP)",
    )
    tg_id = Column(
        "tg_id",
        TEXT,
        nullable=False,
        unique=True,
        index=True,
        doc="User's Telegram id"
    )
    username = Column(
        "username",
        TEXT,
        nullable=True,
        unique=False,
        doc="User's username.",
    )
    group = Column(
        "group",
        TEXT,
        nullable=False,
        unique=False,
        doc="User's group"
    )
    
    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
