import sentry_sdk

from create_bot import bot, dp
from config import TOKEN_SENTRY
# import handlers
from handlers import (admin, commands, dev, menu, prime, reg, settings, stats,
                      student, super_admin, teacher, user)
from middlewares.messagemiddlewares import (UpdateDataCallbackQeryMiddleware,
                                            UpdateDataMessageMiddleware)

sentry_sdk.init(
    dsn=TOKEN_SENTRY,
    traces_sample_rate=1.0,
)


async def register_middleware() -> None:
    dp.message.middleware.register(UpdateDataMessageMiddleware())
    dp.callback_query.middleware.register(UpdateDataCallbackQeryMiddleware())


async def register_handlers() -> None:
    dp.include_router(admin.router)
    dp.include_router(commands.router)
    dp.include_router(dev.router)
    dp.include_router(menu.router)
    dp.include_router(prime.router)
    dp.include_router(reg.router)
    dp.include_router(settings.router)
    dp.include_router(stats.router)
    dp.include_router(super_admin.router)
    dp.include_router(teacher.router)
    dp.include_router(user.router)
    dp.include_router(student.router)


async def register_task() -> None:
    pass


async def on_startup() -> None:
    await register_task()
    await register_middleware()
    await register_handlers()
    print("Bot Online")


async def start_bot():
    await on_startup()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
