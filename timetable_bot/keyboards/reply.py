from aiogram.types import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
)


def create_smile_kb() -> ReplyKeyboardMarkup:
    button_face = KeyboardButton("🤠")
    btn_now = KeyboardButton("что щас")
    btn_today = KeyboardButton("что сёдня")
    btn_week = KeyboardButton("неделя")
    btn_group = KeyboardButton("выбрать группу")

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(button_face)
    kb.row(btn_now)
    kb.row(btn_today, btn_week)
    kb.row(btn_group)
    return kb


nothing = ReplyKeyboardRemove()
smile_kb = create_smile_kb()
