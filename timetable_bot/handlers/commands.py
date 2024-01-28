import asyncio
from aiogram import types, Router, F, Bot
from aiogram.filters import Command
from datetime import timedelta
import logging

import timetable_bot.keyboards as kb
import timetable_bot.utils as utils
from timetable_bot.config import DefaultSettings
from timetable_bot.schemas import TextResponse


config = DefaultSettings()
TD = timedelta(hours=config.TIMEZONE_OFFSET)
main_router = Router(name="main_router")


@main_router.message(Command('start'))
async def send_hello(message: types.Message):
    """
    Приветствие с клавиатурой выбора дня недели.
    """
    await message.reply(TextResponse.greet(message.from_user.first_name), reply_markup=kb.smile_kb)
    await message.answer(TextResponse.SEE_MENU, reply_markup=kb.group_sel_kb)


@main_router.message(Command('week'))
async def send_week_schedule(message: types.Message):
    """
    Отправляет расписание на неделю для группы юзера 
    """
    group = await utils.get_user_group(message.from_user.id)
    result = utils.get_week(group)
    await message.reply(result, reply_markup=kb.day_sel_kb)


@main_router.message(Command('day'))
async def get_day_schedule(message: types.Message):
    """
    Выдаёт клаву с выбором дня, вызывается командой /day (ну или другой из __init__)
    """
    await message.reply(TextResponse.CHOOSE_DAY, reply_markup=kb.day_sel_kb)


@main_router.message(Command('now'))
async def get_current_class(message: types.Message):
    """
    Отправляет текущее занятие (или следующее, если сейчас ничего не идёт)
    """
    group = await utils.get_user_group(message.from_user.id)
    result = utils.get_current_class(group, message.date + TD)
    await message.reply(result)


@main_router.message(Command('next'))
async def get_next_class(message: types.Message):
    """
    Отправляет следущее занятие
    """
    group = await utils.get_user_group(message.from_user.id)
    result = utils.get_next_class(group, message.date + TD)
    await message.reply(result)


@main_router.message(Command('today'))
async def get_today_schedule(message: types.Message):
    """
    Отправляет расписание на сегодня с инлайн переключателем дней недели.
    """
    group = await utils.get_user_group(message.from_user.id)
    result = utils.get_today(group, message.date + TD)
    today = utils.weekday_from_date(message.date + TD)
    if group:
        await message.reply(result, reply_markup=kb.day_switch_kb(utils.weekday_to_weeknum(today)))
    else:
        await message.reply(result)


@main_router.message(Command('tomorrow'))
async def get_tomorrow_schedule(message: types.Message):
    """
    Отправляет расписание на завтра с инлайн переключателем дней недели.
    """
    group = await utils.get_user_group(message.from_user.id)
    result = utils.get_today(group, message.date + timedelta(hours=24) + TD)
    today = utils.weekday_from_date(message.date + timedelta(hours=24) + TD)
    if group:
        await message.reply(result, reply_markup=kb.day_switch_kb(utils.weekday_to_weeknum(today)))
    else:
        await message.reply(result)


@main_router.message(Command('setgr'))
async def set_user_group(message: types.Message):
    """
    Отправляет сообщение с инлайн клавой для выбора группы
    """
    result = "выбери группу из списка:"
    await message.reply(result, reply_markup=kb.group_sel_kb)


@main_router.message(Command('me'))
async def get_user_group(message: types.Message):
    """
    Отправляет сообщение с группой юзера + хранящуююся информацию + текущее время бота
    """
    result = await utils.get_user_group_message(message.from_user.id, message.date + TD)
    await message.reply(result)


@main_router.message(Command('del'))
async def del_me_from_db(message: types.Message):
    """
    Удаляет юзера из бд
    """
    result = await utils.del_user_from_db(message.from_user.id)
    await message.reply(result)


@main_router.message()
async def send_echo(message: types.Message):
    """
    Обработчик следующих команд от юзера (которые можно отправить с reply клавы smile_kb)
    """
    match message.text:
        case "что щас":
            await get_current_class(message)
        case "next пара":
            await get_next_class(message)
        case "что сёдня":
            await get_today_schedule(message)
        case "что завтра":
            await get_tomorrow_schedule(message)
        case "выбрать группу":
            await set_user_group(message)
        case "неделя":
            await send_week_schedule(message)
        case "информация...":
            await get_user_group(message)
        case _:
            await message.reply(
                TextResponse.echo_and_dayselect(
                    message.from_user.first_name,
                    message.text
                ),
                reply_markup=kb.day_sel_kb
            )
