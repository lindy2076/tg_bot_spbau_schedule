from enum import Enum


class DayTitles(str, Enum):
    mon = "Понедельник"
    tue = "Вторник"
    wed = "Среда"
    thu = "Четверг"
    fri = "Пятница"
    sat = "Суббота"
    sun = "Воскресенье"

    @classmethod
    def from_str(cls, day_str):
        for k, v in cls.__members__.items():
            if v == day_str:
                return cls[k]
        return None


class Groups(str, Enum):
    f1_1 = "101.1"
    f1_2 = "101.2"
    b1_1 = "102.1"
    f2_1 = "201.1"
    f2_2 = "201.2"
    b2_1 = "202.1"
    f3_1 = "301.1"
    f3_2 = "301.2"
    f3_3 = "301.3"
    b3_1 = "302.1"
    b3_2 = "302.2"
    f4_1 = "401.1"
    f4_2 = "401.2"
    f4_3 = "401.3"
    b4 = "402"
    m1 = "501"
    m2 = "502"
    m3 = "503"
    m4 = "504"

    @classmethod
    def from_str(cls, day_str):
        for k, v in cls.__members__.items():
            if v == day_str:
                return cls[k]
        return None
