from aiogram import Bot, Dispatcher
from alerts_in_ua import AsyncClient as AsyncAlertsClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from translate import Translator

from config import TOKEN, TOKEN_ALERT

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()
alerts_client = AsyncAlertsClient(token=TOKEN_ALERT)
scheduler = AsyncIOScheduler(timezone="Europe/Kiev")
translator = Translator(to_lang="uk")
