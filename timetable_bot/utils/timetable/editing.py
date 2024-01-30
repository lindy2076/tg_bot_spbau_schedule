import json
from typing import Tuple
import logging
from pydantic import ValidationError

from timetable_bot.schemas import DayTitles, Groups, ErrorMessages, Day
from timetable_bot import utils


def parse_edit_params(params: list[str]) -> Tuple[Tuple[Groups, DayTitles], ErrorMessages]:
    """
    Спарсить параметры команды edit (группа и день)
    """
    if len(params) != 3:
        return None, "чего-то не хватает. /edit group day"

    try:
        day = int(params[2])
        if day > 6 or day < 0:
            raise ValueError
    except ValueError:
        return None, "день введён неправильно. можно 0-6"
    day_title = utils.weeknum_to_weekday(day)
    group = Groups.from_str(params[1])
    if group is None:
        return None, f"группы {params[1]} нет."
    
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
        return "на этот день расписания нет"
    
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
        return None, f"failed to load json {e}"
    
    try:
        Day(**day_json)
    except ValidationError:
        return None, f"failed to validate json."

    day_title = day_json["title"]
    for day in week_json['week_activities']:
        if day['title'] == day_title:
            break
    else:
        return None, "странно однако этого дня нет"
    day["activities"] = day_json["activities"]
    # write to file

    filename = "schedule_json/" + user_group + ".json"
    try:
        with open(filename, 'w', encoding='utf8') as wsch:
            json.dump(week_json, wsch, indent=4, ensure_ascii=False)
            wsch.write("\n")
    except Exception as e:
        return None, f"ошибка во время записи: {e}"
    logging.info(f"расписание {user_group.value} обновлено")
    return week_json, None
