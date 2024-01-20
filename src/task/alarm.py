import asyncio

import asyncache
import cachetools
from aiogram import Bot
from alerts_in_ua import AsyncClient as AsyncAlertsClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import TOKEN_ALERT
from src.data_base import Database


class Alerts:
    def __init__(self, bot: Bot) -> None:
        self.alerts_client = AsyncAlertsClient(token=TOKEN_ALERT)
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone="Europe/Kiev")
        self.scheduler.add_job(self.wait_start_alarm, "interval", seconds=20, id="wait_start_alarm")
        self.scheduler.start()

    @asyncache.cached(cachetools.TTLCache(1, 20))
    async def alert_func(self):
        # Достаю список областей у яких повітряна тривога типу air_raid
        active_alerts = await self.alerts_client.get_active_alerts()
        filtered_alerts = active_alerts.filter("location_type", "oblast", "alert_type", "air_raid")

        list_alerts_oblast_title = []
        for title in filtered_alerts:
            list_alerts_oblast_title.append(title.location_title)
        list_alerts_oblast_title.sort()

        # Перевірка чи є у Волинській області тривога?
        if "Волинська область" in list_alerts_oblast_title:
            our_oblast = True
        else:
            our_oblast = False

        return our_oblast

    async def wait_start_alarm(self):
        db = await Database.setup()

        is_active = await self.alert_func()
        if not is_active:
            return

        self.scheduler.remove_job("wait_start_alarm")
        self.scheduler.add_job(
            self.wait_finish_alarm, "interval", seconds=20, id="wait_finish_alarm"
        )

        all_user_ids = map(lambda e: e[0], await db.list_id_student_agreed_alert())
        await asyncio.gather(*map(self.send_notification(is_active=is_active), all_user_ids))

    async def wait_finish_alarm(self):
        db = await Database.setup()

        is_active = await self.alert_func()
        if is_active:
            return

        self.scheduler.remove_job("wait_finish_alarm")
        self.scheduler.add_job(self.wait_start_alarm, "interval", seconds=20, id="wait_start_alarm")

        all_user_ids = map(lambda e: e[0], await db.list_id_student_agreed_alert())
        await asyncio.gather(*map(self.send_notification(is_active=is_active), all_user_ids))

    def send_notification(self, is_active: bool):
        async def wrapped(user_id: int):
            try:
                text = "Тривога! 🔴" if is_active else "Відбій! 🟢"
                await self.bot.send_message(chat_id=user_id, text=text)
            except:
                await self.bot.send_message(chat_id=2138964363, text=f"{user_id} blocked bot")

        return wrapped
