from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup
)
from aiogram.utils.callback_data import CallbackData

from timetable_bot.schemas import Groups, DayTitles
from timetable_bot.utils import weeknum_to_short_weekday 


def create_group_sel_inline_kb(grd: CallbackData) -> InlineKeyboardMarkup:
    b1011 = InlineKeyboardButton(Groups.f1_1.value + " ⚛️", callback_data=grd.new(id=Groups.f1_1.value))
    b1012 = InlineKeyboardButton(Groups.f1_2.value + " ⚛️", callback_data=grd.new(id=Groups.f1_2.value))
    b1021 = InlineKeyboardButton(Groups.b1_1.value + " 🧬", callback_data=grd.new(id=Groups.b1_1.value))

    f3011 = InlineKeyboardButton(Groups.f3_1.value + " ⚛️", callback_data=grd.new(id=Groups.f3_1.value))
    f3012 = InlineKeyboardButton(Groups.f3_2.value + " ⚛️", callback_data=grd.new(id=Groups.f3_2.value))
    f3013 = InlineKeyboardButton(Groups.f3_3.value + " ⚛️", callback_data=grd.new(id=Groups.f3_3.value))
    b3021 = InlineKeyboardButton(Groups.b3_1.value + " 🧬", callback_data=grd.new(id=Groups.b3_1.value))
    b3022 = InlineKeyboardButton(Groups.b3_2.value + " 🧬", callback_data=grd.new(id=Groups.b3_2.value))

    group_sel_kb = InlineKeyboardMarkup()
    group_sel_kb.row(b1011, b1012)
    group_sel_kb.row(b1021)
    group_sel_kb.row(f3011, f3012, f3013)
    group_sel_kb.row(b3021, b3022)

    return group_sel_kb


def create_weekday_sel_kb(grd: CallbackData) -> InlineKeyboardMarkup:
    b1 = InlineKeyboardButton("пн", callback_data=grd.new(id=DayTitles.mon.value))
    b2 = InlineKeyboardButton("вт", callback_data=grd.new(id=DayTitles.tue.value))
    b3 = InlineKeyboardButton("ср", callback_data=grd.new(id=DayTitles.wed.value))
    b4 = InlineKeyboardButton("чт", callback_data=grd.new(id=DayTitles.thu.value))
    b5 = InlineKeyboardButton("пт", callback_data=grd.new(id=DayTitles.fri.value))
    b6 = InlineKeyboardButton("сб", callback_data=grd.new(id=DayTitles.sat.value))
    
    kb = InlineKeyboardMarkup()
    kb.row(b1, b4)
    kb.row(b2, b5)
    kb.row(b3, b6)
    return kb


def create_wd_arrows_kb(grd: CallbackData, curr_day: int) -> InlineKeyboardMarkup:
    if curr_day == 6:
        left_day, right_day = 5, 0
    else:
        left_day = (curr_day - 1) % 6
        right_day = (curr_day + 1) % 6
    curr_day_str = weeknum_to_short_weekday(curr_day)
    b1 = InlineKeyboardButton("◀️", callback_data=grd.new(where=left_day))
    b2 = InlineKeyboardButton("▶️", callback_data=grd.new(where=right_day))
    b3 = InlineKeyboardButton("🗓️ {:s}".format(curr_day_str), callback_data=grd.new(where="menu"))
    kb = InlineKeyboardMarkup()
    kb.row(b1, b3, b2)
    return kb


def day_switch_kb(curr_day: int) -> InlineKeyboardMarkup:
    kb = create_wd_arrows_kb(day_switch_callback_data, curr_day)
    return kb 


def create_callback_data(k: str = "group"):   # FIXME вспомнить че это
    d = CallbackData("setgr", "id")
    match k:
        case "group":
            d = CallbackData("setgr", "id")
        case "day":
            d = CallbackData("day", "id")
        case "wd":
            d = CallbackData("wd", "where")
    return d


group_callback_data = create_callback_data(k="group")
day_callback_data = create_callback_data(k="day")
day_switch_callback_data = create_callback_data(k="wd")

group_sel_kb = create_group_sel_inline_kb(group_callback_data)
day_sel_kb = create_weekday_sel_kb(day_callback_data)
