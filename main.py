from aiogram.utils.executor import start_webhook
from data_base.controller_db import bd_Start
import os
from create_bot import bot,dp
from handlers import admin, client, super_admin, other

#FSM - Машина стану
#MemoryStorage - клас який допомагає зберігати тимчасові дані в ОЗУ


APP_URL = os.getenv('APP_URL')

async def regiseter_handlers():
    other.register_handler_other(dp)
    admin.register_handler_admin(dp)
    super_admin.register_handler_sadmin(dp)
    client.register_handler_client(dp)

async def on_startup(dp):
    await bot.set_webhook(APP_URL)
    await regiseter_handlers()
    print("BOT ONLINE")
    bd_Start()
    

async def on_shutdown(dp):
    await bot.delete_webhook()
    pass


def start_bot():
    start_webhook(
        dispatcher=dp,
        webhook_path='',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
        host = '0.0.0.0',
        port = int(os.environ.get("WEBHOOK_PORT", 8000)))



