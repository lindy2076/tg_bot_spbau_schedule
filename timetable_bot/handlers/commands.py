from aiogram import types
from datetime import timedelta

import timetable_bot.keyboards as kb
import timetable_bot.utils as utils
from timetable_bot.config import DefaultSettings


TD = timedelta(hours=DefaultSettings().TIMEZONE_OFFSET)

async def send_hello(message: types.Message):
    """
    Приветствие с клавиатурой выбора дня недели.
    """
    await message.reply("ПРИВЕТ, " + str(message.from_user.first_name) + " 🤗🤗🤗",
        reply_markup=kb.smile_kb)
    await message.answer("\nпосмотри в меню, там команды всякие. но пока можешь выбрать свою группу:", 
        reply_markup=kb.group_sel_kb)


async def send_echo(message: types.Message):
    """
    Обработчик следующих команд от юзера (которые можно отправить с reply клавы smile_kb)
    """
    match message.text:
        case "что щас":
            await get_current_class(message)
        case "что сёдня":
            await get_today_schedule(message)
        case "выбрать группу":
            await set_user_group(message)
        case "неделя":
            await send_week_schedule(message)
        case _:
            await message.reply(message.from_user.first_name + " говорит: " + message.text + "\nвыбери день:", reply_markup=kb.day_sel_kb)


async def send_week_schedule(message: types.Message):
    """
    Отправляет расписание на неделю для группы юзера 
    """
    group = await utils.get_user_group(message.from_user.id)
    result = await utils.get_week(group)
    await message.reply(result, reply_markup=kb.day_sel_kb)


async def get_day_schedule(message: types.Message):
    """
    Выдаёт клаву с выбором дня, вызывается командой /day (ну или другой из __init__)
    """
    await message.reply("выбери день.\n", reply_markup=kb.day_sel_kb)


async def get_current_class(message: types.Message):
    """
    Отправляет текущее занятие (или следующее, если сейчас ничего не идёт)
    """
    group = await utils.get_user_group(message.from_user.id)
    result = await utils.get_current_class(group, message.date + TD)
    await message.reply(result)


async def get_today_schedule(message: types.Message):
    """
    Отправляет расписание на сегодня с инлайн переключателем дней недели.
    """
    group = await utils.get_user_group(message.from_user.id)
    result = await utils.get_today(group, message.date + TD)
    today = utils.weekday_from_date(message.date + TD)
    if group:
        await message.reply(result, reply_markup=kb.day_switch_kb(utils.weekday_to_weeknum(today)))
    else:
        await message.reply(result)


async def set_user_group(message: types.Message):
    """
    Отправляет сообщение с инлайн клавой для выбора группы
    """
    result = "выбери группу из списка:"
    await message.reply(result, reply_markup=kb.group_sel_kb)


async def get_user_group(message: types.Message):
    """
    Отправляет сообщение с группой юзера
    """
    result = await utils.get_user_group_message(message.from_user.id)
    await message.reply(result)


async def del_me_from_db(message: types.Message):
    """
    Удаляет юзера из бд
    """
    result = await utils.del_user_from_db(message.from_user.id)
    await message.reply(result)
