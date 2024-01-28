import json 
import datetime
from typing import Tuple

from timetable_bot.schemas import Week, User
from timetable_bot.schemas import (
    Groups, DayTitles, ErrorMessages, TextResponse
)
from timetable_bot.db.models import User as DbUser
from timetable_bot.db.connection import get_session
from .time import weekday_from_date, get_curr_time, get_class_ends_time

from pydantic import ValidationError

from sqlalchemy import delete, select


def load_week_from_file(user_group: Groups) -> Tuple[Week, ErrorMessages | None]:
    """
    Грузим расписание группы user_group и выдаём расписание на неделю.
    Если не выбрана группа или нет расписания, то вернёт соответствующую
    ошибку вторым параметром, иначе None.
    """
    if not user_group:
        return None, ErrorMessages.NO_GROUP

    filename = "schedule_json/" + user_group + ".json"
    try:
        with open(filename) as wsc:
            loaded = json.load(wsc)
    except:
        return None, ErrorMessages.NO_SCHEDULE_FOR_GROUP

    try:
        res = Week(**loaded)
    except:
        return None, ErrorMessages.NO_SCHEDULE_FOR_GROUP
    return res, None


def get_week(user_group: Groups) -> str:
    """
    Даёт расписание на неделю для выбранной группы в готовом виде.
    """
    week, err = load_week_from_file(user_group)
    if err is not None:
        return err
    
    activities = [" " + repr(x) + "\n" for x in week.week_activities]  # FIXME как-то в метод перенести
    return " ".join(activities)


def get_day(user_group: Groups, user_day: DayTitles) -> str:  # FIXME переделать, особенно for else
    """
    Даёт расписание на конкретный день для выбранной группы
    """
    week, err = load_week_from_file(user_group)
    if err is not None:
        return err

    for day in week.week_activities:
        if day.title == user_day:
            break
    else:
        return TextResponse.NO_SCHEDULE_FOR_DAY
    activities = ["    " + repr(x) + "\n" for x in day.activities]

    return user_day + ":\n\n " + " ".join(activities)


def get_today(user_group: Groups, user_datetime: datetime.datetime) -> str:
    """
    Даёт расписание на сегодня для выбранной группы.
    """
    user_day = weekday_from_date(user_datetime)
    return get_day(user_group, user_day)


def get_current_class(user_group: Groups, user_datetime: datetime.datetime) -> str:
    """
    Даёт текущее занятие или будущее занятие на сегодня.
    """
    week, err = load_week_from_file(user_group)
    if err is not None:
        return err

    user_day = weekday_from_date(user_datetime)
    for day in week.week_activities:
        if day.title == user_day:
            break
    else:
        return TextResponse.DAY_NOTHING

    curr_time: str = get_curr_time(user_datetime)
    for _class in day.activities:
        class_time = _class.starts
        class_ends = get_class_ends_time(_class.starts, _class.lasts)
        if class_time < curr_time and curr_time < class_ends:
            return TextResponse.curr_class(_class.name, _class.auditory)
        if curr_time < class_time:
            return TextResponse.future_class(_class.name, _class.auditory, class_time)
    return TextResponse.CURR_CLASS_NONE


def get_next_class(user_group: Groups, user_datetime: datetime.datetime) -> str:
    """
    Даёт следующее занятие на сегодня.
    """
    week, err = load_week_from_file(user_group)
    if err is not None:
        return err

    user_day = weekday_from_date(user_datetime)
    for day in week.week_activities:
        if day.title == user_day:
            break
    else:
        return TextResponse.DAY_NOTHING

    curr_time: str = get_curr_time(user_datetime)
    for _class in day.activities:
        class_time = _class.starts
        class_ends = get_class_ends_time(_class.starts, _class.lasts)
        if class_time < curr_time and curr_time < class_ends:
            continue
        if curr_time < class_time:
            return TextResponse.future_class(_class.name, _class.auditory, class_time)
    return TextResponse.NEXT_CLASS_NONE


async def set_user_group(tg_user, group: str) -> str:  #FIXME описать структуру message в комменте
    """
    Устанавливаем выбранную группу для юзера
    """
    try:
        validated = User(id=tg_user.id, group=group)
    except ValidationError:
        return ErrorMessages.GROUP_DOESNT_EXIST

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
            return TextResponse.SAME_GROUP_CHOSEN
        user_db.group = validated.group
        session.add(user_db)
    await session.commit()
    await session.close()
    return TextResponse.new_group(validated.group)


async def get_user_group_message(user_id: int, user_datetime: datetime.datetime) -> str:
    """
    Смешной текст с номером группы и тем что хранит бот + текущее время бота
    """
    group = await get_user_group(user_id)
    if not group:
        return TextResponse.CHOOSE_GROUP_POLITE
    return TextResponse.info_and_policy(group) + TextResponse.curr_time(
        weekday_from_date(user_datetime), get_curr_time(user_datetime)
    )


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
    return TextResponse.USER_DELETED
