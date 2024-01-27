import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from timetable_bot.config import DefaultSettings
from timetable_bot.handlers import main_router, callback_router


dp = Dispatcher()
settings = DefaultSettings()


def get_app() -> Bot:
    """
    Get application instance.
    """
    BOT_TOKEN = settings.BOT_TOKEN
    logging.info(BOT_TOKEN)
    if not BOT_TOKEN:
        logging.ERROR("No token provided...")
        exit(1)
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    return bot


logging.basicConfig(
    format='%(levelname)s:%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filename='spbau_sch.log',
    level=logging.INFO
)


async def main():
    bot = get_app()
    dp.include_routers(main_router, callback_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())