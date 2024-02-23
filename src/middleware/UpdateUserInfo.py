from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.handlers.user import user_update_db


class MessageMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: Dict[str, Any],
    ) -> Any:
        if message.chat.type == "private":
            await user_update_db(
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username,
            )

            return await handler(message, data)


class CallbackQueryMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        query: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        if query.message.chat.type == "private":
            if not query.data == "Про мене 👀":
                await user_update_db(
                    query.from_user.id,
                    query.from_user.first_name,
                    query.from_user.last_name,
                    query.from_user.username,
                )

            return await handler(query, data)
