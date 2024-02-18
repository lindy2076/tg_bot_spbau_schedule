from pydantic import BaseModel, validator
from typing import List, Dict, Set, Optional

from .enums import DayTitles, Groups


class Subject(BaseModel):
    starts: str
    lasts: str
    name: str
    auditory: str | None
    professor: str | None

    def __repr__(self):
        res = "• <b>{:s}: {:s}</b> | {:s} | {:s} минут | {:s}".format(
            self.starts, self.name, self.auditory,
            str(int(float(self.lasts) * 60)), self.professor
        )
        return res

    @validator('lasts')
    def hours_must_have_dot(cls, v):
        new_v = v
        if '.' not in new_v:
            new_v += '.0'
        try:
            float(new_v)
        except ValueError:
            raise ValueError("Длительность пары не соответствует офрмату")
        return new_v

    @validator('starts')
    def starts_must_have_colon(cls, v):
        if ':' not in v:
            raise Exception
        return v


class Day(BaseModel):
    title: DayTitles
    activities: List[Subject] | None

    def __repr__(self):
        activities_str = ["    " + repr(x) + "\n" for x in self.activities]
        return "🗓 <b>{:s}</b>\n{:s}".format(
            str(self.title), ''.join(activities_str)
        )

    class Config:
        use_enum_values = True


class Week(BaseModel):
    group: Groups
    week_activities: List[Day] | None

    def __repr__(self):
        activities_str = [repr(x) for x in self.week_activities]
        return "\n".join(activities_str)

    class Config:
        use_enum_values = True


class User(BaseModel):
    id: int
    group: Groups

    class Config:
        use_enum_values = True


class Professor(BaseModel):
    name: str
    groups: Set[Groups]
    days: Dict[DayTitles, Set[str]] | None
    subjects: Dict[str, Set[Groups]] | None

    def __repr__(self):
        sg = [f"    • {s} у {', '.join(sorted(gs))}\n" for s, gs in self.subjects.items()]
        ds = [f"    - {d}: {'; '.join(sorted(ts))}\n" for d, ts in self.days.items()]
        return f"🎩 <b>{self.name}</b> ведёт предметы:\n{''.join(sg)}🕰 Ведёт пары в это время:\n{''.join(ds)}"

    def repr_for_day(self, day: DayTitles) -> str:
        sg = [f"    • {s} у {', '.join(sorted(gs))}\n" for s, gs in self.subjects.items()]
        ds = '; '.join(self.days[day])
        return f"🎩 <b>{self.name}</b> ведёт предметы:\n{''.join(sg)}🕰 Ведёт пары в это время:\n     <b>{ds}</b>\n"

    class Config:
        use_enum_value = True
