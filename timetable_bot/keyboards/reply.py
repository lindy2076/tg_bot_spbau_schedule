from aiogram.types import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_smile_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    buttons = ["что щас", "next пара", "что сёдня", "что завтра",
               "неделя", "преподы", "выбрать группу", "🤠 help"]

    for btn_text in buttons:
        builder.button(text=btn_text)

    builder.adjust(2, 2, 2, 2)

    return builder.as_markup(resize_keyboard=True)


def create_yes_no_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = ["да", "нет"]
    for btn_text in buttons:
        builder.button(text=btn_text)
    return builder.as_markup(resize_keyboard=True)


nothing = ReplyKeyboardRemove()
smile_kb = create_smile_kb()
yes_or_no_kb = create_yes_no_kb()
