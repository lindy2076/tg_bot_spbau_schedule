import logging

from aiogram import Router, types, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import timetable_bot.keyboards as kb
from timetable_bot.config import DefaultSettings
from timetable_bot.schemas import TextResponse, LogMessage
from timetable_bot import utils
from .states import SendAdminForm, EditForm, PdfUpdForm


admin_router = Router(name='admin_router')
config = DefaultSettings()

F_from_admin = F.from_user.id == int(config.ADMIN_ID)


@admin_router.message(Command('cancel'))
async def cancel_state(message: types.Message, state: FSMContext):
    """
    Выход из всех состояний.
    """
    curr_state = await state.get_state()
    if curr_state is None:
        await message.reply("нет состояний.")
        return

    await state.clear()
    await message.reply("отмена", reply_markup=kb.smile_kb)


@admin_router.message(Command('send_all'), F_from_admin)
async def send_all(message: types.Message, bot: Bot):
    """
    Разослать всем юзезрам сообщение.
    """
    if len(message.text) < 10:
        await message.answer(TextResponse.NOTHING_SENT)
        return
    id_list = await utils.get_users_ids()
    send_to_count = 0
    for user_id in id_list:
        try:
            await bot.send_message(
                chat_id=int(user_id), text=message.text[10:]
            )
            send_to_count += 1
        except Exception as e:
            logging.info(LogMessage.err_send_all(e))
            await message.answer(f"{user_id} меня заблочил.")
    await message.reply(TextResponse.sent_successfully_to(send_to_count))


@admin_router.message(Command('send_admin'))
async def send_admin(message: types.Message, state: FSMContext):
    """
    Запуск состояния для отправки сообщения админу
    """
    await state.set_state(SendAdminForm.wait_for_message)
    await message.reply(TextResponse.WRITE_MESSAGE_FOR_ADMIN)


@admin_router.message(SendAdminForm.wait_for_message)
async def send_admin_await(message: types.Message, state: FSMContext):
    """
    Ожидание сообщения, последняя проверка перед отправкой.
    Вшивка chat_id и msg_id в сообщение для админа
    """
    await state.update_data(
        wait_for_message=TextResponse.echo_user_msg_for_admin(message)
    )
    await state.set_state(SendAdminForm.confirm)
    await message.reply(
        TextResponse.check_msg_before_sending(message),
        reply_markup=kb.yes_or_no_kb
    )


@admin_router.message(SendAdminForm.confirm)
async def send_admin_confirm(message: types.Message, bot: Bot, state: FSMContext):
    """
    Обработка решения юзера
    """
    if message.text.lower() in ["да", "Да"]:
        data = await state.get_data()
        await bot.send_message(
            chat_id=int(config.ADMIN_ID),
            text=data["wait_for_message"],
        )
        await message.reply(
            TextResponse.MESSAGE_SENT_SUCCESSFULLY,
            reply_markup=kb.smile_kb
        )
        logging.info(LogMessage.sent_msg2admin(message))
    else:
        await message.reply(
            TextResponse.MESSAGE_WASNT_SENT,
            reply_markup=kb.smile_kb
        )
    await state.clear()


@admin_router.message(Command('edit'), F_from_admin)
async def edit_schedule(message: types.Message, state: FSMContext):
    """
    Запуск изменения расписания. Необходимые параметры:
    /edit group day, где day - weeknum (0-6).
    Переходит в состояние EditForm.edit, если команда валидна.
    """
    params = message.text.split()
    params, err = utils.parse_edit_params(params)
    if err is not None:
        await message.reply(err)
        return

    group, day = params
    res = utils.get_day_json(group, day)
    await message.answer(
        TextResponse.group_day_and_day_json(group.value, day.value, res)
    )
    await state.update_data(day=day)
    await state.update_data(group=group)
    await state.set_state(EditForm.edit)


@admin_router.message(EditForm.edit)
async def process_new_dict(message: types.Message, state: FSMContext):
    """
    Проверка отправленного словаря и замена дня в расписании.
    """
    logging.info(message.text)
    data = await state.get_data()
    group = data["group"]

    day_json_str = message.text
    res, err = utils.replace_day_json(day_json_str, group)
    if err is not None:
        await message.reply(f"произошла ошипка. {err}")
        return

    await state.clear()
    await message.reply(f"ok. {str(res)}")


@admin_router.message(Command('pdfupd'), F_from_admin)
async def update_pdf(message: types.Message, state: FSMContext):
    """
    Инициация загрузки pdf
    """
    await message.reply("выберите степень: 0 - bak, 1 - mag, 2 - asp")
    await state.set_state(PdfUpdForm.select_degree)


@admin_router.message(PdfUpdForm.select_degree)
async def update_pdf(message: types.Message, state: FSMContext):
    """
    Инициация загрузки pdf
    """
    if message.text not in ["0", "1", "2"]:
        await message.reply("эээ")
        return
    await state.update_data(select_degree=message.text)
    await message.reply("прикрепите pdf")
    await state.set_state(PdfUpdForm.wait_for_pdf)


@admin_router.message(PdfUpdForm.wait_for_pdf)
async def process_new_pdf(message: types.Message, state: FSMContext, bot: Bot):
    """
    Обработка загрузки pdf
    """
    if not message.document:
        await message.reply("нужен pdf!")
        return
    data = await state.get_data()

    file_id = message.document.file_id
    err = utils.update_pdf_id(file_id, int(data["select_degree"]))
    if err is not None:
        await message.reply(f"{err}")
        return
    await state.clear()
    await message.reply("ok")
    await bot.send_document(message.chat.id, file_id)


@admin_router.message(F.reply_to_message & F_from_admin)
async def reply_user(message: types.Message, bot: Bot):
    """
    Ответить юзеру, который отправил сообщение админу
    """
    params, err = utils.get_chat_and_msg_id(message.reply_to_message)
    if err is not None:
        await message.reply(f"ошипка: {err}. не могу ответить")
    chat_id, msg_id = params
    try:
        await bot.send_message(
                chat_id=chat_id, text=TextResponse.echo_msg_from_admin(message.text),
                reply_to_message_id=msg_id
            )
        await message.reply("ответил")
    except Exception as e:
        await message.reply(f"ошипка отправки: {e}")
