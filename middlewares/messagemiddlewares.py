from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Awaitable, Dict, Any
from handlers.user import user_update_db
from data_base import Database

class UpdateDataMessageMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not message.text == "/me":
            await user_update_db(
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username,
            )

        return await handler(message, data)

class UpdateDataCallbackQeryMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        query: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        db = await Database.setup()
        if not await db.user_exists_sql(query.from_user.id):
            await query.answer("Напишіть боту /start", show_alert=True)
            return
        
        if not query.data == "Про мене 👀" and not query.data == "/me":
            await user_update_db(
                query.from_user.id,
                query.from_user.first_name,
                query.from_user.last_name,
                query.from_user.username,
            )

        return await handler(query, data)