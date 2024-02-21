import asyncio
from aiogram import types, Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import timedelta

import timetable_bot.keyboards as kb
import timetable_bot.utils as utils
from timetable_bot.config import DefaultSettings
from timetable_bot.schemas import TextResponse
from .states import SearchProfessor


config = DefaultSettings()
TD = timedelta(hours=config.TIMEZONE_OFFSET)
main_router = Router(name="main_router")


@main_router.message(Command('start'))
async def send_hello(message: types.Message):
    """
    Приветствие с клавиатурой выбора дня недели.
    """
    await message.reply(TextResponse.greet(message.from_user.first_name),
                        reply_markup=kb.smile_kb)
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
async def select_day(message: types.Message):
    """
    Выдаёт клаву с выбором дня, вызывается командой /day или callback menu
    """
    await message.reply(TextResponse.CHOOSE_DAY, reply_markup=kb.day_sel_kb)


@main_router.message(Command('now'))
async def get_current_class(message: types.Message):
    """
    Отправляет текущее занятие (или следующее, если сейчас ничего не идёт)
    """
    group = await utils.get_user_group(message.from_user.id)
    result = utils.get_current_class(group, message.date + TD)
    await message.reply(result, reply_markup=kb.smile_kb)


@main_router.message(Command('next'))
async def get_next_class(message: types.Message):
    """
    Отправляет следущее занятие
    """
    group = await utils.get_user_group(message.from_user.id)
    result = utils.get_next_class(group, message.date + TD)
    await message.reply(result, reply_markup=kb.smile_kb)


def get_weekday_for_group(user_group, user_datetime):
    """
    Метод хелпер для get_today_schedule
    Возвращает расписание на выбранный день (user_datetime)
    а также сам день.
    """
    result = utils.get_today(user_group, user_datetime)
    today = utils.weekday_from_date(user_datetime)
    return result, today


@main_router.message(Command('today'))
async def get_today_schedule(message: types.Message):
    """
    Отправляет расписание на сегодня с инлайн переключателем дней недели.
    """
    group = await utils.get_user_group(message.from_user.id)
    result, today = get_weekday_for_group(group, message.date + TD)
    reply_kb = None
    if group:
        reply_kb = kb.day_switch_kb(utils.weekday_to_weeknum(today))
    await message.reply(result, reply_markup=reply_kb)


@main_router.message(Command('tomorrow'))
async def get_tomorrow_schedule(message: types.Message):
    """
    Отправляет расписание на завтра с инлайн переключателем дней недели.
    """
    group = await utils.get_user_group(message.from_user.id)
    result, today = get_weekday_for_group(
        group, message.date + timedelta(hours=24) + TD
    )
    reply_kb = None
    if group:
        reply_kb = kb.day_switch_kb(utils.weekday_to_weeknum(today))
    await message.reply(result, reply_markup=reply_kb)


@main_router.message(Command('setgr'))
async def set_user_group(message: types.Message):
    """
    Отправляет сообщение с инлайн клавой для выбора группы
    """
    await message.reply(
        TextResponse.CHOOSE_GROUP2, reply_markup=kb.group_sel_kb
    )


@main_router.message(Command('me'))
@main_router.message(Command('help'))
async def get_user_group(message: types.Message):
    """
    Отправляет сообщение с группой юзера + хранящуююся информацию
    + текущее время бота + четность недели
    """
    result = await utils.get_user_group_message(
        message.from_user.id, message.date + TD
    )
    await message.reply(result, link_preview_options=types.LinkPreviewOptions(is_disabled=True))


@main_router.message(Command('del'))
async def del_me_from_db(message: types.Message):
    """
    Удаляет юзера из бд
    """
    result = await utils.del_user_from_db(message.from_user.id)
    await message.reply(result)


@main_router.message(Command('pdf'))
async def serve_pdf(message: types.Message, bot: Bot):
    file_id, err = utils.get_pdf_id()
    if err is not None:
        await message.reply(err, reply_markup=kb.smile_kb)
        return
    await bot.send_document(message.chat.id, file_id,
                            reply_markup=kb.select_degree_pdf,
                            caption=TextResponse.THIS_IS_BACH_SCHEDULE)


@main_router.message(Command('faculty'))
async def send_faculty_info(message: types.Message):
    group = await utils.get_user_group(message.from_user.id)
    if group is None:
        await set_user_group(message)
        return
    user_profs = utils.get_user_profs_resp(group)
    await message.answer(user_profs, reply_markup=kb.faculty_kb1())


@main_router.message(SearchProfessor.search)
async def handle_search_professor(message: types.Message, state: FSMContext):
    """
    Вытащить ключевые слова и попытаться найти кого-нибудь из преподов...
    """
    if not message.text:
        await message.reply(TextResponse.MSG_IS_NOT_TEXT)
        return
    result, err = utils.search_profs_by_keywords(message.text)
    if err is not None:
        await message.reply(err + "\nдля выхода из поиска /cancel")
        return
    await message.reply(result, reply_markup=kb.faculty_kb1("allnow", after_search=True))
    await state.clear()


@main_router.message(F.text)
async def send_echo(message: types.Message, bot: Bot):
    """
    Обработчик следующих команд от юзера
    (которые можно отправить с reply клавы smile_kb)
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
        case "преподы":
            await send_faculty_info(message)
        case "🤠 help":
            await get_user_group(message)
        case "pdf":
            await serve_pdf(message, bot)
        case _:
            await message.reply(
                TextResponse.echo_and_dayselect(
                    message.from_user.first_name,
                    message.text
                ),
                reply_markup=kb.day_sel_kb
            )


@main_router.message(F.sticker)
async def manage_nonmsg(message: types.Message):
    """
    Обработка сообщений от юзера без текста.
    """
    await message.answer_sticker(sticker=TextResponse.SPECIAL_STICKER_FILE_ID)
