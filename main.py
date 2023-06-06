# import
import os

# import sentry_sdk
import logging
import sentry_sdk
import asyncio
import datetime

# from import
from create_bot import dp
from aiogram import types
from handlers import admin, client, reg, super_admin, menu, stats, commands, prime, dev
from create_bot import scheduler
from task import alarm

from aiogram.utils.executor import start_polling

APP_URL = os.getenv("APP_URL")

sentry_sdk.init(
    dsn="https://53565fef30db43dc9498abf76cf91604@o4504669478780928.ingest.sentry.io/4505244319088640",
    traces_sample_rate=1.0,
)


async def logs():
    # Формування назви файлу з датою
    filename = f"logs\Аpp_Error.log"

    # Налаштування об'єкта логування
    logging.basicConfig(
        level=logging.ERROR,
        filename=filename,
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


async def register_handlers():
    reg.register_handler_reg(dp)
    dev.register_handler_dev(dp)
    admin.register_handler_admin(dp)
    super_admin.register_handler_sadmin(dp)
    menu.register_handler_menu(dp)
    stats.register_handler_stats(dp)
    commands.register_handler_commands(dp)
    await prime.register_handler_stats(dp)
    client.register_handler_client(dp)


async def register_task():
    await alarm.create_task_alarm()


async def on_startup(dp):
    await logs()
    await register_task()
    await register_handlers()
    scheduler.start()
    print("Bot Online")


async def on_shutdown(dp):
    print("Bot Offline")


def start_bot():
    start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
    )
