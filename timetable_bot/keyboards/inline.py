from aiogram.types import (
    InlineKeyboardMarkup
)
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from timetable_bot.schemas import Groups
from timetable_bot.utils import weeknum_to_short_weekday, weeknum_to_weekday


PHY_EMOJI = " ⚛️"
BIO_EMOJI = " 🧬"


def determine_emoji(group: Groups):
    if group.value.split(".")[0][-1] == "1":
        return PHY_EMOJI
    return BIO_EMOJI


class SelectGroupCallback(CallbackData, prefix="setgr"):
    id: str


class SelectDayCallback(CallbackData, prefix="day"):
    id: str


class SwitchDayCallback(CallbackData, prefix="wd"):
    where: str


def add_group_button(builder: InlineKeyboardBuilder, year: list[Groups]):
    for group in year:
        builder.button(
            text=group.value + determine_emoji(group),
            callback_data=SelectGroupCallback(id=group.value).pack()
        )


def create_group_sel_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    year1 = [Groups.f1_1, Groups.f1_2, Groups.b1_1]
    add_group_button(builder, year1)
    
    year2 = [Groups.f2_1, Groups.f2_2, Groups.b2_1]
    add_group_button(builder, year2)

    year3 = [Groups.f3_1, Groups.f3_2, Groups.f3_3, Groups.b3_1, Groups.b3_2]
    add_group_button(builder, year3)
    
    year4 = [Groups.f4_1, Groups.f4_2, Groups.f4_3, Groups.b4]
    add_group_button(builder, year4)

    builder.adjust(len(year1), len(year2), 3, 2, len(year4))
    return builder.as_markup()


def create_weekday_sel_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    btns = ["пн", "вт", "ср", "чт", "пт", "сб"]
    for idx, btn_text in enumerate(btns):
        builder.button(
            text=btn_text,
            callback_data=SelectDayCallback(id=weeknum_to_weekday(idx).value).pack()
        )
    builder.adjust(2, 2, 2)
    return builder.as_markup()


def create_wd_arrows_kb(curr_day: int) -> InlineKeyboardMarkup:
    if curr_day == 6:
        left_day, right_day = 5, 0
    else:
        left_day = (curr_day - 1) % 6
        right_day = (curr_day + 1) % 6
    curr_day_str = weeknum_to_short_weekday(curr_day)

    builder = InlineKeyboardBuilder()
    builder.button(text="◀️", callback_data=SwitchDayCallback(where=str(left_day)).pack())
    builder.button(
        text="🗓️ {:s}".format(curr_day_str),
        callback_data=SwitchDayCallback(where="menu").pack()
    )
    builder.button(text="▶️", callback_data=SwitchDayCallback(where=str(right_day)).pack())

    return builder.as_markup()


def day_switch_kb(curr_day: int) -> InlineKeyboardMarkup:
    kb = create_wd_arrows_kb(curr_day)
    return kb


group_sel_kb = create_group_sel_inline_kb()
day_sel_kb = create_weekday_sel_kb()
