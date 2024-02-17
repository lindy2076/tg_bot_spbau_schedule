import json
from typing import Tuple
import logging
from pydantic import ValidationError

from timetable_bot.schemas import (
    DayTitles, Groups, Day, ErrorMessages, TextResponse
)
from timetable_bot import utils
from timetable_bot.config import DefaultSettings


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
    filename = filename = "schedule_json/" + user_group + ".json"
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

    return f"<pre><code class='language-json'>{day}</code></pre>"


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
        logging.info(f"failed to load json. {e}")
        return None, f"failed to load json. {e}"

    try:
        Day(**day_json)
    except ValidationError:
        return None, "failed to validate json."

    day_title = day_json["title"]
    for day in week_json['week_activities']:
        if day['title'] == day_title:
            break
    else:
        return None, "странно однако этого дня нет"
    day["activities"] = day_json["activities"]

    filename = "schedule_json/" + user_group + ".json"
    try:
        with open(filename, 'w', encoding='utf8') as wsch:
            json.dump(week_json, wsch, indent=4, ensure_ascii=False)
            wsch.write("\n")
    except Exception as e:
        return None, f"ошибка во время записи: {e}"
    logging.info(f"расписание {user_group.value} обновлено")
    return week_json, None


def update_pdf_id(file_id: str, degree: int = 0) -> ErrorMessages:
    """
    Обновляет file_id пдфки с расписанием в файле pdffileid
    """
    filename = config.FILE_FOR_PDF_FILE_ID
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        while len(lines) < 3:
            lines.append("\n")
        lines[degree] = f"{file_id}\n"
        with open(filename, 'w') as f:
            f.writelines(lines)

    except Exception as e:
        logging.info(f"ошибка записи file_id. {e}")
        return "ошипка записи"
    return None
