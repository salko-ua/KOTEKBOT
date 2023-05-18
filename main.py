# import
import os
#import sentry_sdk
import logging

# from import
from create_bot import dp
#from config import TOKEN_SENTRY
from aiogram.utils.executor import start_polling
from handlers import admin, client, reg, super_admin, menu, stats, commands, prime
from create_bot import scheduler
from schedulers import task, alarm
APP_URL = os.getenv("APP_URL")


#logging.basicConfig(level=logging.INFO)



async def register_handlers():
    reg.register_handler_reg(dp)
    admin.register_handler_admin(dp)
    super_admin.register_handler_sadmin(dp)
    menu.register_handler_menu(dp)
    stats.register_handler_stats(dp)
    commands.register_handler_commands(dp)
    await prime.register_handler_stats(dp)
    client.register_handler_client(dp)

async def register_task():
    await task.create_task_main()
    await alarm.create_task_alarm()

async def on_startup(dp):
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
        skip_updates=True
    )
