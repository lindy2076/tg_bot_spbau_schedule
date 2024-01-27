from aiogram.types import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_smile_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    buttons = ["🤠", "что щас", "next пара", "что сёдня", "неделя", "выбрать группу", "информация..."]

    for btn_text in buttons:
        builder.button(text=btn_text)

    builder.adjust(1, 2, 2, 2)

    return builder.as_markup(resize_keyboard=True)


nothing = ReplyKeyboardRemove()
smile_kb = create_smile_kb()
