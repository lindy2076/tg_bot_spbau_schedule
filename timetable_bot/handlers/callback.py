import datetime as dt
import logging
from aiogram import types, Router, Bot, F
from aiogram.fsm.context import FSMContext

import timetable_bot.utils as utils
import timetable_bot.keyboards as kb
from timetable_bot.config import DefaultSettings
from timetable_bot.schemas import TextResponse, DayTitles, LogMessage
from .states import SearchProfessor


callback_router = Router(name="callback_router")
config = DefaultSettings()


@callback_router.callback_query(kb.SelectGroupCallback.filter(F.ctx == "own"))
async def handle_user_group(call: types.CallbackQuery,
                            callback_data: kb.SelectGroupCallback):
    """
    Отвечаем на нажатие инлайн клавы с выбором группы (меняем группу)
    """
    res = await utils.set_user_group(call.from_user, callback_data.id)
    await call.message.answer(res, reply_markup=kb.smile_kb)
    await call.answer()


@callback_router.callback_query(kb.SelectGroupCallback.filter(F.ctx == "other"))
async def handle_user_group2(call: types.CallbackQuery,
                             callback_data: kb.SelectGroupCallback):
    """
    Отвечаем на нажатие инлайн клавы с выбором группы (не меняем группу)
    """
    group = callback_data.id
    user_dt = dt.datetime.now(
        dt.timezone(dt.timedelta(hours=config.TIMEZONE_OFFSET))
    )
    day4button = utils.weekday_to_weeknum(utils.weekday_from_date(user_dt))
    result = TextResponse.schedule_for_another_group(
        utils.get_today(group, user_dt), group
    )
    await call.message.edit_text(result, reply_markup=kb.day_switch_kb(day4button, group))  # TODO
    await call.answer()


@callback_router.callback_query(kb.SelectDayCallback.filter(F.ctx == "sch"))
async def handle_day_select_sch(call: types.CallbackQuery,
                                callback_data: kb.SelectDayCallback):
    """
    Отвечаем на нажатие инлайн клавы с выбором дня недели (для своего расписания)
    """
    group = await utils.get_user_group(call.from_user.id)
    if not group:
        await call.message.answer(
            TextResponse.CHOOSE_GROUP, reply_markup=kb.group_sel_kb
        )
    else:
        day = callback_data.id
        user_dt = dt.datetime.now(
            dt.timezone(dt.timedelta(hours=config.TIMEZONE_OFFSET))
        )
        result = utils.get_day(
            group, DayTitles.from_str(day_str=day), utils.week_is_odd(user_dt)
        )
        day_for_button = utils.weekday_to_weeknum(day)
        await call.message.edit_text(
            result, reply_markup=kb.day_switch_kb(day_for_button)
        )

    await call.answer()


@callback_router.callback_query(kb.SelectDayCallback.filter(F.ctx == "fac"))
async def handle_day_select_fac(call: types.CallbackQuery,
                                callback_data: kb.SelectDayCallback):
    """
    Отвечаем на нажатие инлайн клавы с выбором дня недели (для поиска преподов)
    """
    group = await utils.get_user_group(call.from_user.id)
    if not group:
        await call.message.answer(
            TextResponse.CHOOSE_GROUP, reply_markup=kb.group_sel_kb
        )
    else:
        day = callback_data.id
        res = utils.get_all_profs_in_day_resp(DayTitles.from_str(day_str=day))
        await call.message.edit_text(res, reply_markup=kb.faculty_kb1("my"))
    await call.answer()


@callback_router.callback_query(kb.SelectDayCallback.filter())
async def handle_day_select_group(call: types.CallbackQuery,
                                  callback_data: kb.SelectDayCallback):
    """
    Отвечаем на нажатие инлайн клавы с выбором дня недели (не для своего расписания)
    """
    group = callback_data.ctx
    user_dt = dt.datetime.now(
            dt.timezone(dt.timedelta(hours=config.TIMEZONE_OFFSET))
    )
    result = utils.get_day(
        group, DayTitles.from_str(day_str=callback_data.id), utils.week_is_odd(user_dt)
    )
    day_for_button = utils.weekday_to_weeknum(callback_data.id)

    await call.message.edit_text(
        TextResponse.schedule_for_another_group(result, group),
        reply_markup=kb.day_switch_kb(day_for_button, context=group)
    )
    await call.answer()


@callback_router.callback_query(kb.SwitchDayCallback.filter())
async def handle_day_switch(call: types.CallbackQuery,
                            callback_data: kb.SwitchDayCallback):
    """
    Отвечаем на нажатие инлайн клавы с переключением дня недели
    """
    group = await utils.get_user_group(call.from_user.id)
    if not group:
        await call.message.answer(
            TextResponse.CHOOSE_GROUP, reply_markup=kb.group_sel_kb
        )
    else:
        button_pressed = utils.parse_day_switch_data(callback_data.where)
        if button_pressed == "menu":
            reply_kb = kb.create_weekday_sel_kb(context=callback_data.ctx)
            msg = TextResponse.CHOOSE_DAY
        elif button_pressed == "groups":
            reply_kb = kb.group_sel_kb_other
            msg = TextResponse.CHOOSE_GROUP_TO_LOOK
        else:
            new_day = button_pressed
            if callback_data.ctx == "sch":
                reply_kb = kb.day_switch_kb(new_day)
                user_dt = dt.datetime.now(
                    dt.timezone(dt.timedelta(hours=config.TIMEZONE_OFFSET))
                )
                msg = utils.get_day(
                    group,
                    utils.weeknum_to_weekday(new_day),
                    utils.week_is_odd(user_dt)
                )
            elif callback_data.ctx == "fac":
                reply_kb = kb.faculty_kb1("my", new_day)
                msg = utils.get_all_profs_in_day_resp(utils.weeknum_to_weekday(new_day))
            else:  # callback_data.ctx is a group number
                user_dt = dt.datetime.now(
                    dt.timezone(dt.timedelta(hours=config.TIMEZONE_OFFSET))
                )
                reply_kb = kb.day_switch_kb(new_day, callback_data.ctx)
                msg = TextResponse.schedule_for_another_group(
                    utils.get_day(
                        callback_data.ctx,
                        utils.weeknum_to_weekday(new_day),
                        utils.week_is_odd(user_dt)
                    ),
                    callback_data.ctx
                )
        try:
            await call.message.edit_text(msg, reply_markup=reply_kb)
        except Exception as e:
            logging.debug(LogMessage.same_msg_didnt_edit(e))
    await call.answer()


@callback_router.callback_query(kb.SelectDegreeForPdfCB.filter())
async def handle_degree_pdf_select(call: types.CallbackQuery,
                                   callback_data: kb.SelectDegreeForPdfCB,
                                   bot: Bot):
    """
    Ответ на колбек с инлайн клавы для выбора пдфки
    """
    selected_degree = callback_data.degree
    file_id, err = await utils.get_pdf_id(degree=selected_degree)
    if err is not None:
        await call.message.answer(err)
    else:
        await bot.send_document(call.message.chat.id, file_id,
                                reply_markup=kb.smile_kb)
    await call.answer()


@callback_router.callback_query(kb.FacultyCallback.filter())
async def handle_faculty_kb_sel(call: types.CallbackQuery,
                                callback_data: kb.FacultyCallback, state: FSMContext):
    """
    Ответ на колбек клавы kb.faculty_kb1
    """
    state_curr = callback_data.curr
    if state_curr == "my":
        user_dt = dt.datetime.now(
            dt.timezone(dt.timedelta(hours=config.TIMEZONE_OFFSET))
        )
        today = utils.weekday_to_weeknum(utils.weekday_from_date(user_dt))
        res = utils.get_all_profs_today_resp(user_dt)
        await call.message.edit_text(res, reply_markup=kb.faculty_kb1("my", today))
    elif state_curr == "allnow":
        group = await utils.get_user_group(call.from_user.id)
        if not group:
            await call.message.edit_text(
                TextResponse.CHOOSE_GROUP, reply_markup=kb.group_sel_kb
            )
        else:
            res = utils.get_user_profs_resp(group)
            await call.message.edit_text(res, reply_markup=kb.faculty_kb1("allnow"))
    elif state_curr == "search":
        await call.message.answer(TextResponse.ENTER_KEYWORDS)
        await state.set_state(SearchProfessor.search)

    await call.answer()
