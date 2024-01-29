from aiogram import Router, types, Bot
from aiogram.filters import Command

from timetable_bot.config import DefaultSettings
from timetable_bot.schemas import TextResponse
from timetable_bot import utils


admin_router = Router(name='admin_router')
config = DefaultSettings()


@admin_router.message(Command('send_all'))
async def send_all(message: types.Message, bot: Bot):
    if str(message.from_user.id) != config.ADMIN_ID:
        await message.answer(TextResponse.YOU_ARE_NOT_ADMIN)
        return
    if len(message.text) < 10:
        await message.answer("ничего не отправлено. пусто!")
        return
    id_list = await utils.get_users_ids()
    send_to_count = 0
    for user_id in id_list:
        try:
            await bot.send_message(chat_id=int(user_id), text=message.text[10:])
            send_to_count += 1
        except:
            await message.answer(user_id + " меня заблочил.")
    await message.reply("вроде отправилось. Всего " + str(send_to_count))
