import json
import logging
from pydantic import ValidationError
from sqlalchemy import select
from typing import Tuple

from timetable_bot import utils
from timetable_bot.config import DefaultSettings

from timetable_bot.db.connection import get_session
from timetable_bot.db.models import Schedule as DbSchedule

from timetable_bot.schemas import (
    DayTitles, Groups, Day, ErrorMessages, TextResponse, LogMessage, Degree
)


config = DefaultSettings()


def parse_edit_params(
    params: list[str]
) -> Tuple[Tuple[Groups, DayTitles], ErrorMessages]:
    """
    Спарсить параметры команды edit (группа и день)
    """
    if len(params) != 3:
        return None, ErrorMessages.EDIT_MISSING_PARAMS

    try:
        day = int(params[2])
        if day > 6 or day < 0:
            raise ValueError
    except ValueError:
        return None, ErrorMessages.EDIT_WRONG_DAY
    day_title = utils.weeknum_to_weekday(day)
    group = Groups.from_str(params[1])
    if group is None:
        return None, ErrorMessages.no_such_group(params[1])

    return (group, day_title), None


def get_week_json(user_group: Groups) -> Tuple[dict, ErrorMessages]:
    """
    Выдаёт json недели в виде словаря
    """
    filename = "schedule_json/" + user_group + ".json"
    try:
        with open(filename) as wsch:
            loaded = json.load(wsch)
    except Exception as e:
        logging.info(f"Failed to load {filename}. Error: {e}")
        return None, ErrorMessages.NO_SCHEDULE_FOR_GROUP

    return loaded, None


def get_day_json(user_group: Groups, user_day: DayTitles) -> str:
    """
    Выдаёт расписание на день в виде json строки
    """
    week, err = get_week_json(user_group)
    if err is not None:
        return err

    for day in week['week_activities']:
        if day['title'] == user_day:
            break
    else:
        return TextResponse.NO_SCHEDULE_FOR_DAY

    return f"{day}"


def replace_day_json(
    day_json_str: str, user_group: Groups
) -> Tuple[dict, ErrorMessages]:
    """
    Берёт json msg и пытается поменять её в расписании.
    """
    week_json, err = get_week_json(user_group)
    if err is not None:
        return None, err

    try:
        day_json = json.loads(day_json_str.replace("'", "\""))
    except Exception as e:
        logging.info(ErrorMessages.json_load_failed(e))
        return None, ErrorMessages.json_load_failed(e)

    try:
        Day(**day_json)
    except ValidationError:
        return None, ErrorMessages.INVALID_JSON

    day_title = day_json["title"]
    for day in week_json['week_activities']:
        if day['title'] == day_title:
            break
    else:
        return None, ErrorMessages.IMPOSSIBLE_DAY_NOT_FOUND
    day["activities"] = day_json["activities"]

    filename = "schedule_json/" + user_group + ".json"
    try:
        with open(filename, 'w', encoding='utf8') as wsch:
            json.dump(week_json, wsch, indent=4, ensure_ascii=False)
            wsch.write("\n")
    except Exception as e:
        return None, ErrorMessages.failed_to_write(e)
    logging.info(LogMessage.schedule_updated(user_group.value))
    return week_json, None


async def update_by_pdf_id(
    file_id: str, degree: Degree, description: str = ""
) -> None:
    """
    Добавляет новую запись в таблицу shedule или обновляет старую по file_id
    """
    session = await get_session()
    q = select(DbSchedule).where(DbSchedule.tg_id == file_id)
    existing_schedule_info = await session.scalar(q)
    if not existing_schedule_info:
        new_schedule_info = DbSchedule(
            tg_id=file_id, degree=degree, description=description
        )
        session.add(new_schedule_info)
    else:
        existing_schedule_info.degree = degree
        existing_schedule_info.description = description
        session.add(existing_schedule_info)
    await session.commit()
    await session.close()
