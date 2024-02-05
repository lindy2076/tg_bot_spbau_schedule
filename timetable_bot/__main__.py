import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler, setup_application
)

from timetable_bot.config import DefaultSettings
from timetable_bot.handlers import (
    admin_router, main_router, callback_router
)


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


async def on_startup_polling(bot: Bot):
    logging.info("bot started with longpolling!")


async def on_startup_webhook(bot: Bot):
    logging.info("bot started with webhook!")
    await bot.set_webhook(
        settings.WEBHOOK_URL,
        certificate=FSInputFile(settings.CERT_PATH),
    )


async def main_longpolling():
    dp.startup.register(on_startup_polling)
    await dp.start_polling(
        bot,
        on_startup=on_startup_polling,
    )


def main_webhook():
    dp.startup.register(on_startup_webhook)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="0.0.0.0", port=8080)  # ip inside docker


if __name__ == "__main__":
    logging.basicConfig(
        format='%(levelname)s:%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        filename='spbau_sch.log',
        level=logging.INFO
    )
    bot = get_app()
    dp.include_routers(admin_router, main_router, callback_router)

    if settings.DEBUG in ["TRUE", "True", "1", True]:
        asyncio.run(main_longpolling())
    else:
        main_webhook()
