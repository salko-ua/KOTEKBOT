# from import
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN, token_alert
from alerts_in_ua import AsyncClient as AsyncAlertsClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from translate import Translator


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
alerts_client = AsyncAlertsClient(token=token_alert)
scheduler = AsyncIOScheduler(timezone="Europe/Kiev")
translator = Translator(to_lang="uk")
