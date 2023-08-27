import json 
import datetime
from typing import Tuple

from timetable_bot.schemas import Degree, Week, User
from timetable_bot.schemas import Degrees, Groups, DayTitles, ErrorMessages
from timetable_bot.db.models import User as DbUser
from timetable_bot.db.connection import get_session
from .time import weekday_from_date, get_curr_time, get_class_ends_time

from pydantic import ValidationError

from sqlalchemy import delete, select


def get_degree(user_group: Groups) -> Degrees:  # зачем..? скорее всего depricated
    """
    Определяем степень челика по номеру группы (бак, маг, асп, null)
    """
    if not user_group:
        return Degrees.null
    if user_group[0] <= "4":
        return Degrees.bach
    if user_group[0] in ["5", "6"]:
        return Degrees.mag
    return Degrees.null


async def load_week_from_file(user_group: Groups) -> Tuple[list[Week], ErrorMessages | None]:
    """
    Грузим расписание группы user_group и выдаём расписание на неделю.
    Если не выбрана группа или нет расписания, то вернёт соответствующую
    ошибку вторым параметром, иначе None.
    """
    degree = get_degree(user_group)
    if degree == Degrees.null:
        return None, ErrorMessages.NO_GROUP

    filename = "schedule_json/" + user_group + ".json"
    try:
        with open(filename) as wsc:
            loaded = json.load(wsc)
    except:
        return None, ErrorMessages.NO_SCHEDULE

    res = Degree(**loaded)
    return getattr(res, "activities"), None


async def get_week(user_group: Groups) -> str:
    """
    Даёт расписание на неделю для выбранной группы в готовом виде.
    """
    week_activities, err = await load_week_from_file(user_group)
    if err is not None:
        return err

    for _group in week_activities:   # чзх 
        if _group.group != user_group:
            continue
        activities = [" " + repr(x) + "\n" for x in _group.week_activities]   # FIXME как-то в метод перенести
        return " ".join(activities)
    return "пока для этой группы расписания нет..."


async def get_day(user_group: Groups, user_day: DayTitles) -> str:  # FIXME переделать, особенно for else
    """
    Даёт расписание на конкретный день для выбранной группы
    """
    bach_activities, err = await load_week_from_file(user_group)
    if err is not None:
        return err

    for _group in bach_activities:
        if _group.group == user_group:
            break
    else:
        return "пока для этой группы расписания нет..."
    
    for activity in _group.week_activities:
        if activity.title == user_day:
            break
    else:
        return "на этот день расписания нет..."
    activities = ["    " + repr(x) + "\n" for x in activity.activities]

    return user_day + ":\n\n " + " ".join(activities)


async def get_today(user_group: Groups, user_datetime: datetime.datetime) -> str:
    """
    Даёт расписание на сегодня для выбранной группы.
    """
    bach_activities, err = await load_week_from_file(user_group)
    if err is not None:
        return err
    
    for _group in bach_activities:
        if _group.group == user_group:
            break
    else:
        return "пока для этой группы расписания нет..."

    user_day = weekday_from_date(user_datetime)
    for activity in _group.week_activities:
        if activity.title == user_day:
            break
    else:
        return "на этот день расписания нет..."
    activities = ["    " + repr(x) + "\n" for x in activity.activities]

    return user_day + ":\n\n " + " ".join(activities)


async def get_current_class(user_group: Groups, user_datetime: datetime.datetime) -> str:
    """
    Даёт текущее занятие или будущее занятие на сегодня.
    """
    bach_activities, err = await load_week_from_file(user_group)
    if err is not None:
        return err

    for _group in bach_activities:
        if _group.group == user_group:
            break
    else:
        return "пока для этой группы расписания нет..."

    user_day = weekday_from_date(user_datetime)
    for day in _group.week_activities:
        if day.title == user_day:
            break
    else:
        return "НИЧЕГО!!! СВОБОДА!!!"

    curr_time = get_curr_time(user_datetime)
    for _class in day.activities:
        class_time = _class.starts
        class_ends = get_class_ends_time(_class.starts, _class.lasts)
        if class_time < curr_time and curr_time < class_ends:
            return "сейчас идёт " + _class.name + " в " + _class.auditory
        if curr_time < class_time:
            return "сейчас будет " + _class.name + " в " + class_time + " в " + _class.auditory
    return "кажется ничего не идёт..."


async def set_user_group(tg_user, message: str) -> str:  #FIXME описать структуру message в комменте
    """
    Устанавливаем выбранную группу для юзера
    """
    try:
        group = message.split(":")[1]
    except IndexError:
        return "вот ето да... интересно как ты ето сделал... напиши моему автору!"

    try:
        validated = User(id=tg_user.id, group=group)
    except ValidationError:
        return "такой группы нет.. напиши моему автору!"

    session = await get_session()
    user_str = str(tg_user.id) 
    query = select(DbUser).where(DbUser.tg_id == user_str)
    user_db = await session.scalar(query)
    if not user_db:
        new_user = DbUser(
            tg_id=user_str, 
            username=tg_user.first_name,
            group=validated.group
        )
        session.add(new_user)
    else:
        if user_db.group == validated.group:
            await session.close()
            return "кажется ты уже выбрал эту группу..."
        user_db.group = validated.group
        session.add(user_db)
    await session.commit()
    await session.close()
    return "теперь " + validated.group + " - ваша группа"


async def get_user_group_message(user_id: int) -> str:
    """
    Смешной текст с номером группы и тем что хранит бот.
    """
    group = await get_user_group(user_id)
    if not group:
        return "к сожалению, я пока о тебе ничего не знаю. попробуй /setgr *номер_группы*"
    return "я выдаю для тебя расписание группы номер " + group + \
    "\n\nя храню только жизненно необходимую информацию, а именно: " + \
    "айди телеграма, имя в телеграме, номер группы, время обращения, все сообщения боту, время онлайна в телеграме, фамилию в телеграме, вашу платёжную информацию, местоположение, а также номер телефона.\n" +\
    "шучу😁. я храню только ваш тг айди, тг имя, номер группы и время обращения к боту. чтобы удалить себя из базы данных, пропишите /del"


async def get_user_group(user_id: int) -> Groups | None:
    """
    Получаем группу юзера из базы по тг айди.
    """
    session = await get_session()
    query = select(DbUser).where(DbUser.tg_id == str(user_id))
    user_db = await session.scalar(query)
    await session.close()
    if not user_db:
        return None
    return user_db.group


async def del_user_from_db(user_id: int) -> str:
    """
    Удаляем юзера из дб по тг айди.
    """
    session = await get_session()
    query = delete(DbUser).where(DbUser.tg_id == str(user_id))
    await session.execute(query)
    await session.commit()
    await session.close()
    return "тебя больше (а может и не больше) нет в моей бд. (но в логах есть🙃 )"
