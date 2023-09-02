from enum import Enum


class DayTitles(str, Enum):
    mon = "Понедельник"
    tue = "Вторник"
    wed = "Среда"
    thu = "Четверг"
    fri = "Пятница"
    sat = "Суббота"
    sun = "Воскресенье"


class Groups(str, Enum):
    f1_1 = "101.1"
    f1_2 = "101.2"
    b1_1 = "102.1"
    # f2_1 = "201.1"
    # f2_2 = "201.2"
    # b2_1 = "202.1"
    # b2_2 = "202.2"
    # f3_1 = "301.1"
    # f3_2 = "301.2"
    # f3_3 = "301.3"
    b3_1 = "302.1"
    b3_2 = "302.2"
    # f4 = "401"
    # b4 = "402"


class Degrees(str, Enum):
    bach = "bachelor"
    mag = "master"
    asp = "phd"
    null = "null"
