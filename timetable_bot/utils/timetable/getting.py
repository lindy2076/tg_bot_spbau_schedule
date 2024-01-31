import json
import datetime
import logging
from typing import Tuple

from pydantic import ValidationError
from sqlalchemy import delete, select

from timetable_bot.config import DefaultSettings
from timetable_bot.schemas import Week, User, Day
from timetable_bot.schemas import (
    Groups, DayTitles, ErrorMessages, TextResponse
)
from timetable_bot.db.models import User as DbUser
from timetable_bot.db.connection import get_session
from .time import (
    weekday_from_date, get_curr_time, get_class_ends_time, week_is_odd
)


config = DefaultSettings()


def load_week_from_file(user_group: Groups) -> Tuple[Week, ErrorMessages]:
    """
    Грузим расписание группы user_group и выдаём объект расписания на неделю.
    Если не выбрана группа или нет расписания, то вернёт соответствующую
    ошибку вторым параметром, иначе None.
    """
    if not user_group:
        return None, ErrorMessages.NO_GROUP

    filename = "schedule_json/" + user_group + ".json"
    try:
        with open(filename) as wsc:
            loaded = json.load(wsc)
    except Exception as e:
        logging.info(f"Failed to load {filename}. Error: {e}")
        return None, ErrorMessages.NO_SCHEDULE_FOR_GROUP

    try:
        res = Week(**loaded)
    except Exception as e:
        logging.info(f"Failed to validate {filename} data. Error: {e}")
        return None, ErrorMessages.NO_SCHEDULE_FOR_GROUP
    return res, None


def get_week(user_group: Groups) -> str:
    """
    Даёт расписание на неделю для выбранной группы в готовом виде.
    Если группы нет, то выдаёт строку с ошибкой.
    """
    week, err = load_week_from_file(user_group)
    if err is not None:
        return err

    activities = [repr(day) + "\n" for day in week.week_activities]
    return " ".join(activities)


def get_day_obj(week: Week, user_day: DayTitles) -> Tuple[Day, TextResponse]:
    """
    Получем объект расписания на выбранный день в неделе
    """
    for day in week.week_activities:
        if day.title == user_day:
            break
    else:
        return None, TextResponse.NO_SCHEDULE_FOR_DAY
    return day, None


def get_day(
    user_group: Groups,
    user_day: DayTitles,
    week_is_odd: bool = None
) -> str:
    """
    Даёт расписание на конкретный день для выбранной группы в готовом виде.
    """
    week, err = load_week_from_file(user_group)
    if err is not None:
        return err

    day, err = get_day_obj(week, user_day)
    if err is not None:
        return err
    activities = [" "*4 + repr(x) + "\n" for x in day.activities]
    activities_str = ' '.join(activities)
    response = f"{user_day.value}:\n\n{activities_str}"
    if week_is_odd is None:
        return response

    if "чет" in activities_str or "нечет" in activities_str:
        response += f"<i>{TextResponse.curr_week_odd_even(week_is_odd)}</i>"

    return response


def get_today(user_group: Groups, user_datetime: datetime.datetime) -> str:
    """
    Даёт расписание на сегодня для выбранной группы.
    """
    user_day = weekday_from_date(user_datetime)
    return get_day(user_group, user_day, week_is_odd(user_datetime))


def get_current_class(
    user_group: Groups, user_datetime: datetime.datetime
) -> str:
    """
    Даёт текущее занятие или будущее занятие на сегодня.
    """
    week, err = load_week_from_file(user_group)
    if err is not None:
        return err

    user_day = weekday_from_date(user_datetime)
    day, err = get_day_obj(week, user_day)
    if err is not None:
        return err

    curr_time: str = get_curr_time(user_datetime)
    for _class in day.activities:
        class_time = _class.starts
        class_ends = get_class_ends_time(_class.starts, _class.lasts)
        if class_time < curr_time and curr_time < class_ends:
            return TextResponse.curr_class(_class.name, _class.auditory)
        if curr_time < class_time:
            return TextResponse.future_class(
                _class.name, _class.auditory, class_time
            )
    return TextResponse.CURR_CLASS_NONE


def get_next_class(
    user_group: Groups, user_datetime: datetime.datetime
) -> str:
    """
    Даёт следующее занятие на сегодня.
    """
    week, err = load_week_from_file(user_group)
    if err is not None:
        return err

    user_day = weekday_from_date(user_datetime)
    day, err = get_day_obj(week, user_day)
    if err is not None:
        return err

    curr_time: str = get_curr_time(user_datetime)
    for _class in day.activities:
        class_time = _class.starts
        class_ends = get_class_ends_time(_class.starts, _class.lasts)
        if class_time < curr_time and curr_time < class_ends:
            continue
        if curr_time < class_time:
            return TextResponse.future_class(
                _class.name, _class.auditory, class_time
            )
    return TextResponse.NEXT_CLASS_NONE


async def set_user_group(tg_user, group: str) -> str:
    """
    Устанавливаем выбранную группу для юзера

    :param tg_user: Telegram User object
    """
    try:
        validated = User(id=tg_user.id, group=group)
    except ValidationError:
        return ErrorMessages.GROUP_DOESNT_EXIST

    session = await get_session()
    user_id_str = str(tg_user.id)
    query = select(DbUser).where(DbUser.tg_id == user_id_str)
    user_db = await session.scalar(query)
    if not user_db:
        new_user = DbUser(
            tg_id=user_id_str,
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


async def get_user_group_message(
    user_id: int, user_datetime: datetime.datetime
) -> str:
    """
    Смешной текст с номером группы и тем что хранит бот + текущее время бота
    """
    group = await get_user_group(user_id)
    if not group:
        return TextResponse.CHOOSE_GROUP_POLITE
    return TextResponse.info_and_policy(group) + TextResponse.curr_time(
        weekday_from_date(user_datetime), get_curr_time(user_datetime)
    ) + TextResponse.curr_week_odd_even(week_is_odd(user_datetime))


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


async def get_users_ids():
    """
    Получаем список тг айди всех юзеров.
    """
    session = await get_session()
    q = select(DbUser)
    users = await session.execute(q)
    await session.close()
    ids = list(map(lambda u: u[0].tg_id, users))
    return ids


def get_pdf_id() -> Tuple[str, ErrorMessages]:
    """
    Получить file_id пдфки с расписанием.
    """
    filename = config.FILE_FOR_PDF_FILE_ID
    try:
        with open(filename, 'r') as f:
            file_id = f.readline()
    except Exception as e:
        logging.info(f"ошибка чтения file_id. {e}")
        return None, "ошипка чтения. возможно его ещё не загрузили"
    return file_id, None
