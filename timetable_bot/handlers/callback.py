from aiogram import types, Router
import logging

import timetable_bot.utils as utils
import timetable_bot.keyboards as kb
from timetable_bot.schemas import TextResponse


callback_router = Router(name="callback_router")


@callback_router.callback_query(kb.SelectGroupCallback.filter())
async def handle_user_group(call: types.CallbackQuery, 
                            callback_data: kb.SelectGroupCallback):
    """
    Отвечаем на нажатие инлайн клавы с выбором группы (меняем группу)
    """
    res = await utils.set_user_group(call.from_user, callback_data.id)
    await call.message.answer(res, reply_markup=kb.smile_kb)
    await call.answer()


@callback_router.callback_query(kb.SelectDayCallback.filter())
async def handle_day_select(call: types.CallbackQuery,
                            callback_data: kb.SelectDayCallback):
    """
    Отвечаем на нажатие инлайн клавы с выбором дня недели
    """
    group = await utils.get_user_group(call.from_user.id)
    if not group:
        await call.message.answer(TextResponse.CHOOSE_GROUP, reply_markup=kb.group_sel_kb)
    else:
        day = utils.parse_sel_day_data(callback_data.id)
        result = await utils.get_day(group, day)
        day_for_button = utils.weekday_to_weeknum(day)
        try:
            await call.message.edit_text(result, reply_markup=kb.day_switch_kb(day_for_button))
        except:
            logging.warning("same text, didn't edit")
    await call.answer()


@callback_router.callback_query(kb.SwitchDayCallback.filter())
async def handle_day_switch(call: types.CallbackQuery,
                            callback_data: kb.SwitchDayCallback):
    """
    Отвечаем на нажатие инлайн клавы с переключением дня недели
    """
    group = await utils.get_user_group(call.from_user.id)
    if not group:
        await call.message.answer(TextResponse.CHOOSE_GROUP, reply_markup=kb.group_sel_kb)
    else:
        button_pressed = utils.parse_day_switch_data(callback_data.where)
        if button_pressed == "menu":
            reply_kb = kb.day_sel_kb
            msg = TextResponse.CHOOSE_DAY
        else:
            new_day = int(button_pressed)
            reply_kb = kb.day_switch_kb(new_day)
            msg = await utils.get_day(group, utils.weeknum_to_weekday(new_day))

        try:
            await call.message.edit_text(msg, reply_markup=reply_kb)
        except:
            logging.warning("same text, didn't edit")
    await call.answer()
