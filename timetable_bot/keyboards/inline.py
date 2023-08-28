from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup
)
from aiogram.utils.callback_data import CallbackData
from timetable_bot.schemas import Groups, DayTitles


def create_group_sel_inline_kb(grd: CallbackData) -> InlineKeyboardMarkup:
    b1011 = InlineKeyboardButton(Groups.f1.value + " ⚛️", callback_data=grd.new(id=Groups.f1.value))
    b1021 = InlineKeyboardButton(Groups.b1.value + " 🧬", callback_data=grd.new(id=Groups.b1.value))

    b2011 = InlineKeyboardButton(Groups.f2_1.value + " ⚛️", callback_data=grd.new(id=Groups.f2_1.value))
    b2012 = InlineKeyboardButton(Groups.f2_2.value + " ⚛️", callback_data=grd.new(id=Groups.f2_2.value))

    b2021 = InlineKeyboardButton(Groups.b2_1.value + " 🧬", callback_data=grd.new(id=Groups.b2_1.value))
    b2022 = InlineKeyboardButton(Groups.b2_2.value + " 🧬", callback_data=grd.new(id=Groups.b2_2.value))

    b3011 = InlineKeyboardButton(Groups.f3_1.value + " ⚛️", callback_data=grd.new(id=Groups.f3_1.value))
    b3012 = InlineKeyboardButton(Groups.f3_2.value + " ⚛️", callback_data=grd.new(id=Groups.f3_2.value))
    b3013 = InlineKeyboardButton(Groups.f3_3.value + " ⚛️", callback_data=grd.new(id=Groups.f3_3.value))

    b302 = InlineKeyboardButton(Groups.b3.value + " 🧬", callback_data=grd.new(id=Groups.b3.value))

    b401 = InlineKeyboardButton(Groups.f4.value + " ⚛️", callback_data=grd.new(id=Groups.f4.value))
    b402 = InlineKeyboardButton(Groups.b4.value + " 🧬", callback_data=grd.new(id=Groups.b4.value))
    

    group_sel_kb = InlineKeyboardMarkup()
    group_sel_kb.row(b1011, b1021)
    group_sel_kb.row(b2011, b2012)
    group_sel_kb.row(b2021, b2022)
    group_sel_kb.row(b3011, b3012, b3013)
    group_sel_kb.row(b302)
    group_sel_kb.row(b401, b402)
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
    b1 = InlineKeyboardButton("◀️", callback_data=grd.new(where=left_day))
    b2 = InlineKeyboardButton("▶️", callback_data=grd.new(where=right_day))
    b3 = InlineKeyboardButton("🗓️", callback_data=grd.new(where="menu"))
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
