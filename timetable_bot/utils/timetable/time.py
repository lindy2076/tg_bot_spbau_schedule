import datetime

from timetable_bot.schemas import DayTitles


def weeknum_to_weekday(weeknum: int) -> DayTitles:
    match weeknum:
        case 0:
            return DayTitles.mon
        case 1:
            return DayTitles.tue
        case 2:
            return DayTitles.wed
        case 3:
            return DayTitles.thu
        case 4:
            return DayTitles.fri
        case 5:
            return DayTitles.sat
        case 6:
            return DayTitles.sun


def weekday_to_weeknum(weekday: DayTitles) -> int:
    match weekday:
        case DayTitles.mon.value:
            return 0
        case DayTitles.tue.value:
            return 1
        case DayTitles.wed.value:
            return 2
        case DayTitles.thu.value:
            return 3
        case DayTitles.fri.value:
            return 4
        case DayTitles.sat.value:
            return 5
        case DayTitles.sun.value:
            return 6


def parse_sel_day_data(data: str) -> DayTitles:
    """
    Парсим данные callback запроса клавы sel_day_kb.
    """
    try:
        d = data.split(":")[1]
    except:
        return DayTitles.sun
    return d


def parse_day_switch_data(data: str) -> int | str:
    """
    Парсим данные callback запроса клавы day_switch_kb.
    Возвращаем номер дня или "menu"
    """
    try:
        d = int(data.split(":")[1])
    except ValueError:
        # print(data.split(":")[1], type(data.split(":")[1]), e.__class__)
        return "menu"
    except:
        return 6
    return d


def weekday_from_date(user_datetime: datetime.datetime) -> DayTitles:
    """
    Получаем день недели по дате
    """
    weekday_num = user_datetime.weekday()
    return weeknum_to_weekday(weekday_num)


def get_curr_time(user_datetime: datetime.datetime) -> str:
    """
    Конвертируем время user_datetime в строку формата hh:mm
    """
    return "{:02d}:{:02d}".format(user_datetime.hour, user_datetime.minute)


def get_class_ends_time(class_starts: str, class_lasts: str) -> str:
    """
    Считаем время конца пары. Формат строки hh:mm
    """
    start_hour, start_minute = map(int, class_starts.split(":"))
    lasts_in_mins = int(float(class_lasts) * 60)
    start_datetime = datetime.datetime(
        hour=start_hour, minute=start_minute, year=2020, month=1, day=1
    )
    end_datetime = start_datetime + datetime.timedelta(minutes=lasts_in_mins)
    return "{:02d}:{:02d}".format(end_datetime.hour, end_datetime.minute)
