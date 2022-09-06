from aiogram import types
import timetable_bot.utils as utils
import logging

import timetable_bot.keyboards as kb


async def handle_user_group(call: types.CallbackQuery):
    """
    Отвечаем на нажатие инлайн клавы с выбором группы (меняем группу)
    """
    res = await utils.set_user_group(call.from_user, call.data)
    await call.message.answer(res, reply_markup=kb.smile_kb)
    await call.answer()


async def handle_day_select(call: types.CallbackQuery):
    """
    Отвечаем на нажатие инлайн клавы с выбором дня недели
    """
    group = await utils.get_user_group(call.from_user.id)
    if not group:
        await call.message.answer("надо выбрать группу:", reply_markup=kb.group_sel_kb)
        await call.answer()
    else:
        day = utils.parse_sel_day_data(call.data)
        result = await utils.get_day(group, day)
        day_for_button = utils.weekday_to_weeknum(day)
        try:
            await call.message.edit_text(result, reply_markup=kb.day_switch_kb(day_for_button))
        except:
            logging.warning("same text, didn't edit")
        await call.answer()


async def handle_day_switch(call: types.CallbackQuery):
    """
    Отвечаем на нажатие инлайн клавы с переключением дня недели
    """
    group = await utils.get_user_group(call.from_user.id)
    if not group:
        await call.message.answer("надо выбрать группу:", reply_markup=kb.group_sel_kb)
        await call.answer()
    else:
        new_day = utils.parse_day_switch_data(call.data)
        if new_day == "menu":
            try:
                await call.message.edit_text("выбери день.\n", reply_markup=kb.day_sel_kb)
            except:
                logging.warning("same text, didn't edit")
            await call.answer()
        else:
            result = await utils.get_day(group, utils.weeknum_to_weekday(int(new_day)))
            try:
                await call.message.edit_text(result, reply_markup=kb.day_switch_kb(int(new_day)))
            except:
                logging.warning("same text, didn't edit")
            await call.answer()
