from create_bot import scheduler
from handlers.client import alert_func
from create_bot import bot
from  data_base import Database
from aiogram.utils.exceptions import BotBlocked, RetryAfter
from datetime import datetime
import asyncio
import time

async def wait_start_alarm():
    db = await Database.setup()
    
    text, is_active = await alert_func()
    if not is_active:
        return
    
    scheduler.remove_job("wait_start_alarm")
    scheduler.add_job(wait_finish_alarm, "interval", seconds = 25, id = "wait_finish_alarm")
    
    all_user_ids = map(lambda e: e[0], await db.all_user_id_sql())
    await asyncio.gather(*map(send_notification(is_active), all_user_ids))


async def wait_finish_alarm():
    db = await Database.setup()

    text, is_active = await alert_func()
    if is_active:
        return
    
    scheduler.remove_job("wait_finish_alarm")
    scheduler.add_job(wait_start_alarm, "interval", seconds = 25, id = "wait_start_alarm")

    all_user_ids = map(lambda e: e[0], await db.all_user_id_sql())
    await asyncio.gather(*map(send_notification(is_active), all_user_ids))



def send_notification(is_active: bool):
    async def wrapped(user_id: int):
        db = await Database.setup()
        try:
            try:
                await bot.send_sticker(user_id, "CAACAgIAAxkBAAEI_1hkY5y8yh_-0cKFPQ5Sv2SWlYQaCwACLCUAAvF3IUhe2e30dH6RaC8E" if is_active else "CAACAgIAAxkBAAEI_1xkY5zsKG4_LdSX-d2oMY994WAHjQACQisAAssEIUhdsPeRZOOUMC8E")
                await bot.send_message(user_id, "Тривога! 🔴" if is_active else "Відбій! 🟢")
            except RetryAfter as ra:
                await asyncio.sleep(ra.timeout)
        except BotBlocked:
            pass
    
    return wrapped

async def create_task_alarm():
    scheduler.add_job(wait_start_alarm, "interval", seconds = 17, id = "wait_start_alarm")