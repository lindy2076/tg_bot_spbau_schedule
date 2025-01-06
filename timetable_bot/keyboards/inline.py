from aiogram.types import (
    InlineKeyboardMarkup
)
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


from timetable_bot.schemas import Groups
from timetable_bot.schemas import Degree
from timetable_bot.utils import weeknum_to_short_weekday, weeknum_to_weekday


PHY_EMOJI = " ⚛️"
BIO_EMOJI = " 🧬"


def determine_emoji(group: Groups):
    if group.value[0] == "5":
        return " 🧙"
    if group.value.split(".")[0][-1] == "1":
        return PHY_EMOJI
    return BIO_EMOJI


class SelectGroupCallback(CallbackData, prefix="setgr"):
    id: str
    ctx: str


class SelectDayCallback(CallbackData, prefix="day"):
    id: str
    ctx: str


class SwitchDayCallback(CallbackData, prefix="wd"):
    where: str
    ctx: str


class SelectDegreeForPdfCB(CallbackData, prefix="degree_pdf"):
    degree: str


class FacultyCallback(CallbackData, prefix="fc"):
    curr: str


def add_group_button(
    builder: InlineKeyboardBuilder, year: list[Groups], context: str
) -> None:
    for group in year:
        builder.button(
            text=group.value + determine_emoji(group),
            callback_data=SelectGroupCallback(
                id=group.value, ctx=context
            ).pack()
        )


def create_group_sel_inline_kb(context: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    year1 = [Groups.f1_1, Groups.f1_2, Groups.b1_1, Groups.b1_2]
    add_group_button(builder, year1, context=context)

    year2 = [Groups.f2_1, Groups.f2_2, Groups.b2]
    add_group_button(builder, year2, context=context)

    year3 = [Groups.f3_1, Groups.f3_2, Groups.f3_3, Groups.b3]
    add_group_button(builder, year3, context=context)

    year4 = [Groups.f4_1, Groups.f4_2, Groups.f4_3, Groups.b4_1, Groups.b4_2]
    add_group_button(builder, year4, context=context)

    # year5 = [Groups.m1, Groups.m2, Groups.m3, Groups.m4]
    # add_group_button(builder, year5, context=context)

    builder.adjust(len(year1), len(year2), len(year3), len(year4))
    return builder.as_markup()


def create_weekday_sel_kb(context: str = "sch") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    btns = ["пн", "вт", "ср", "чт", "пт", "сб"]
    for idx, btn_text in enumerate(btns):
        builder.button(
            text=btn_text,
            callback_data=SelectDayCallback(
                id=weeknum_to_weekday(idx).value,
                ctx=context
            ).pack()
        )
    builder.adjust(2, 2, 2)
    return builder.as_markup()


def create_wd_arrows_kb_builder(curr_day: int, context: str = "sch") -> InlineKeyboardBuilder:
    if curr_day == 6:
        left_day, right_day = 5, 0
    else:
        left_day = (curr_day - 1) % 6
        right_day = (curr_day + 1) % 6
    curr_day_str = weeknum_to_short_weekday(curr_day)

    builder = InlineKeyboardBuilder()
    builder.button(text="◀️", callback_data=SwitchDayCallback(
        where=str(left_day), ctx=context).pack()
    )
    builder.button(
        text="🗓️ {:s}".format(curr_day_str),
        callback_data=SwitchDayCallback(where="menu", ctx=context).pack()
    )
    builder.button(text="▶️", callback_data=SwitchDayCallback(
        where=str(right_day), ctx=context).pack()
    )

    return builder


def day_switch_kb(curr_day: int, context: str = "sch") -> InlineKeyboardMarkup:
    kb = create_wd_arrows_kb_builder(curr_day, context)
    if context == "sch" or context in {g.value for g in Groups}:
        kb.button(
            text="👀 что там у других групп...",
            callback_data=SwitchDayCallback(where="groups", ctx=context)
        )
        kb.adjust(3, 1)
        if context != "sch":
            kb.button(
                text="моё расписание",
                callback_data=SwitchDayCallback(where=str(curr_day), ctx="sch")
            )
            kb.adjust(3, 2)
    return kb.as_markup()


def create_select_degree_pdf() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="магистры", callback_data=SelectDegreeForPdfCB(
        degree=Degree.mag).pack()
    )
    builder.button(text="аспиранты", callback_data=SelectDegreeForPdfCB(
        degree=Degree.phd).pack()
    )
    return builder.as_markup()


def faculty_kb1(next_: str = "allnow", curr_day: int = 0, after_search: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if next_ == "my":
        builder = create_wd_arrows_kb_builder(curr_day, context="fac")
        builder.button(
            text="все мои преподы",
            callback_data=FacultyCallback(curr="allnow").pack()
        )
        builder.adjust(3, 1)
    elif next_ == "allnow":
        builder.button(
            text="кто где сегодня",
            callback_data=FacultyCallback(curr="my").pack()
        )
    builder.button(
        text=["поискать..", "поискать ещё..."][after_search],
        callback_data=FacultyCallback(curr="search").pack()
    )
    return builder.as_markup()


group_sel_kb = create_group_sel_inline_kb(context="own")
group_sel_kb_other = create_group_sel_inline_kb(context="other")
day_sel_kb = create_weekday_sel_kb()
select_degree_pdf = create_select_degree_pdf()
