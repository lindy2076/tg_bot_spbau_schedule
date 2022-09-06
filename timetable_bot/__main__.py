import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from timetable_bot.config import DefaultSettings
from timetable_bot.handlers import list_of_commands, callback_handlers


def get_app() -> Bot:
    """
    Get application instance.
    """
    settings = DefaultSettings()
    BOT_TOKEN = settings.BOT_TOKEN
    bot = Bot(token=BOT_TOKEN)
    return bot 


async def on_startup(_):
    logging.info("bot started!")


logging.basicConfig(
    format='%(levelname)s:%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p', 
    filename='spbau_sch.log', 
    level=logging.INFO)

bot = get_app()
dp = Dispatcher(bot)

# регистрируем команды
for handler, handler_commands in list_of_commands:
    dp.register_message_handler(handler, commands=handler_commands)
# регистрируем хэндлеры для инлайн кнопок
for handler, handler_filter in callback_handlers:
    dp.register_callback_query_handler(handler, handler_filter)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
