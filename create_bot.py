# from import
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN, token_alert
from alerts_in_ua import AsyncClient as AsyncAlertsClient


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())
alerts_client = AsyncAlertsClient(token = token_alert)
