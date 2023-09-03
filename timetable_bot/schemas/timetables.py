from pydantic import BaseModel, validator
from typing import List

from .enums import DayTitles, Groups


class Subject(BaseModel):
    starts: str
    lasts: str
    name: str
    auditory: str | None
    professor: str | None

    def __repr__(self):
        res = ""
        res += "• " + str(self.starts) + ": " + str(self.name) + " | " + str(self.auditory) + " | " + str(int(float(self.lasts) * 60)) + " минут | " + str(self.professor) + "\n"
        return res
    
    @validator('lasts')
    def hours_must_have_dot(cls, v):
        new_v = v
        if '.' not in new_v:
            new_v += '.0'
        try:
            float(new_v)
        except ValueError:
            raise ValueError("Где-то длительность пары ужасная")   # FIXME norm opisanie
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
        return "\n" + "-"*20 + str(self.title) + "-"*20 + ' \n\n ' + " ".join(activities_str)
    
    class Config:  
        use_enum_values = True


class Week(BaseModel):
    group: Groups
    week_activities: List[Day] | None

    def __repr__(self):
        activities_str = ["  " + repr(x) + "\n" for x in self.week_activities]
        return str(self.group) + ': \n ' + "\n" + " ".join(activities_str)
    
    class Config:  
        use_enum_values = True


# class Degree(BaseModel):
#     degree: Degrees
#     activities: List[Week]

#     def __repr__(self):
#         activities_str = [" " + repr(x) + "\n" for x in self.activities]
#         return str(self.degree) + ': \n' + " ".join(activities_str)

#     class Config:  
#         use_enum_values = True


class User(BaseModel):
    id: int
    group: Groups

    class Config:
        use_enum_values = True
