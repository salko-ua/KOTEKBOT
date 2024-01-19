import asyncio
import logging

import aiogram
import apykuma
import sentry_sdk
from aiogram import Bot, Dispatcher

from src.config import KUMA_TOKEN, TOKEN, TOKEN_SENTRY
from src.handlers import (
    admin,
    commands,
    menu,
    reg,
    settings,
    stats,
    student,
    super_admin,
    user,
)
from src.middleware.UpdateUserInfo import CallbackQueryMiddleware, MessageMiddleware
from src.task.alarm import Alerts

if TOKEN_SENTRY != "":
    sentry_sdk.init(dsn=TOKEN_SENTRY, traces_sample_rate=1.0)


async def register_middleware(dp: aiogram.Dispatcher) -> None:
    dp.message.middleware.register(MessageMiddleware())
    dp.callback_query.middleware.register(CallbackQueryMiddleware())


async def register_handlers(dp: aiogram.Dispatcher) -> None:
    dp.include_router(admin.router)
    dp.include_router(commands.router)
    dp.include_router(menu.router)
    dp.include_router(reg.router)
    dp.include_router(settings.router)
    dp.include_router(stats.router)
    dp.include_router(super_admin.router)
    dp.include_router(user.router)
    dp.include_router(student.router)


async def start_bot() -> None:
    if KUMA_TOKEN != "":
        await apykuma.start(url=KUMA_TOKEN, delay=15)

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dispatcher = Dispatcher()
    Alerts(bot)

    await register_middleware(dispatcher)
    await register_handlers(dispatcher)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_bot())
