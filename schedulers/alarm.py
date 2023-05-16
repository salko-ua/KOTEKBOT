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
    
    print("Чекаю тривогу" + str(datetime.now()))
    text, is_active = await alert_func()
    if not is_active:
        return
    
    scheduler.remove_job("wait_start_alarm")
    scheduler.add_job(wait_finish_alarm, "interval", seconds = 25, id = "wait_finish_alarm")

    start = time.time()
    all_user_ids = map(lambda e: e[0], await db.all_user_id_sql())
    print(all_user_ids)
    await asyncio.gather(*map(send_notification(is_active), all_user_ids))
    end = time.time()
    print(end - start)



async def wait_finish_alarm():
    db = await Database.setup()
    print("Чекаю відбій"+ str(datetime.now()))

    text, is_active = await alert_func()
    if is_active:
        return
    
    scheduler.remove_job("wait_finish_alarm")
    scheduler.add_job(wait_start_alarm, "interval", seconds = 25, id = "wait_start_alarm")

    start = time.time()
    all_user_ids = map(lambda e: e[0], await db.all_user_id_sql())
    await asyncio.gather(*map(send_notification(is_active), all_user_ids))
    end = time.time()
    print(end - start)


def send_notification(is_active: bool):
    async def wrapped(user_id: int):
        db = await Database.setup()
        try:
            try:
                await bot.send_message(user_id, "Повітряна тривога 🚨" if is_active else "Відбій повітряної тривоги 🚨")
                print(f"send {user_id}")
            except RetryAfter as ra:
                await asyncio.sleep(ra.timeout)
        except BotBlocked:
            await db.delete_users_sql(user_id)
            await bot.send_message(5963046063, f"Видалено користувача {user_id}")
    
    return wrapped

async def create_task_alarm():
    scheduler.add_job(wait_start_alarm, "interval", seconds = 17, id = "wait_start_alarm")