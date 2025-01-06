from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID, TEXT
from sqlalchemy.sql import func

from timetable_bot.db import DeclarativeBase


class Schedule(DeclarativeBase):
    __tablename__ = "schedule"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
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
        doc="Schedule file tg_id",
    )
    degree = Column(
        "degree",
        TEXT,
        nullable=False,
        unique=False,
        doc="Degree for which schedule is",
    )
    description = Column(
        "description",
        TEXT,
        nullable=False,
        unique=False,
        doc="Description of the schedule",
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name)
                   for column in self.__table__.columns}
        mapped_str = ", ".join(
            map(lambda x: f"{x[0]}={x[1]}", columns.items())
        )
        return f'<{self.__tablename__}: {mapped_str}>'
