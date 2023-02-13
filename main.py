from aiogram.utils.executor import start_webhook
from data_base.controller_db import bd_Start
import os
from create_bot import bot,dp
from handlers import admin, client, super_admin, other
import sentry_sdk

#FSM - Машина стану
#MemoryStorage - клас який допомагає зберігати тимчасові дані в ОЗУ


APP_URL = os.getenv('APP_URL')

sentry_sdk.init(
    dsn="https://622c27cfc84b46119192ff14073e2df9@o4504669478780928.ingest.sentry.io/4504669483827200",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

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


def start_bot():
    start_webhook(
        dispatcher=dp,
        webhook_path='',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
        host = '0.0.0.0',
        port = int(os.environ.get("WEBHOOK_PORT", 8080)))



