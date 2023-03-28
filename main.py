# import
import os
import sentry_sdk
import logging
# from import
from create_bot import bot, dp
from config import token_sentry
from aiogram.utils.executor import start_webhook
from data_base.controller_db import bd_Start
from handlers import admin, client, other, super_admin, menu, stats, commands


APP_URL = os.getenv("APP_URL")

logging.basicConfig(level=logging.INFO)

sentry_sdk.init(
    dsn=token_sentry,
    traces_sample_rate=1.0,
)


async def regiseter_handlers():
    other.register_handler_other(dp)
    admin.register_handler_admin(dp)
    super_admin.register_handler_sadmin(dp)
    menu.register_handler_menu(dp)
    stats.register_handler_stats(dp)
    commands.register_handler_commands(dp)
    client.register_handler_client(dp)

async def on_startup(dp):
    await bot.set_webhook(APP_URL)
    await regiseter_handlers()
    print("BOT ONLINE")
    await bd_Start()


async def on_shutdown(dp):
    await bot.delete_webhook()


def start_bot():
    start_webhook(
        dispatcher=dp,
        webhook_path="",
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.environ.get("WEBHOOK_PORT", 8000)),
    )
