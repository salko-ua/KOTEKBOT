import asyncio
import datetime

import asyncache
import cachetools

from create_bot import alerts_client, bot, scheduler
from data_base import Database


# =========================== Тривога ===========================
@asyncache.cached(cachetools.TTLCache(1, 20))
async def alert_func():
    delta = datetime.timedelta(hours=2, minutes=0)
    todays = datetime.datetime.now(datetime.timezone.utc) + delta
    hours = todays.strftime("%H")
    minut = todays.strftime("%M")
    second = todays.strftime("%S")

    # Достаю список областей у яких повітряна тривога типу air_raid
    active_alerts = await alerts_client.get_active_alerts()
    filtered_alerts = active_alerts.filter(
        "location_type", "oblast", "alert_type", "air_raid"
    )

    # Достаю список назв областей у яких повітряна тривога
    count = len(filtered_alerts)
    all_alerts = f"🌍 Області з тривогою({count} з 26):\nОновлено : {int(hours)+1}:{minut}:{second}\n\n"
    list_alerts_oblast_title = []
    for title in filtered_alerts:
        list_alerts_oblast_title.append(title.location_title)
    list_alerts_oblast_title.sort()

    # Перевірка чи є у Волинській області тривога?
    if "Волинська область" in list_alerts_oblast_title:
        our_oblast = True
    else:
        our_oblast = False

    # Області які будуть на першому місці
    need_oblast_title = [
        "Тернопільська область",
        "Івано-Франківська область",
        "Хмельницька область",
        "Чернівецька область",
        "Закарпатська область",
        "Львівська область",
        "Рівненська область",
        "Волинська область",
    ]
    # список у якому будуть області які нам підходять за списком вище і у них тривога
    need_oblast_title_list_new = []
    # Цикл пеоевірки через помилку
    for j in range(0, len(need_oblast_title)):
        try:
            list_alerts_oblast_title.index(need_oblast_title[j])
            list_alerts_oblast_title.remove(need_oblast_title[j])
            need_oblast_title_list_new.insert(0, need_oblast_title[j])
        except ValueError:
            await asyncio.sleep(0.05)
    # Роблю гарне повідомлення
    if len(need_oblast_title_list_new) == 0 and len(list_alerts_oblast_title) == 0:
        all_alerts += f" - Тривоги відсутні 🟢\n"
    else:
        if len(need_oblast_title_list_new) == 0:
            all_alerts += f"Західні області :\n • Немає\n\n"
        else:
            all_alerts += f"Західні області :\n"
            for alert in need_oblast_title_list_new:
                all_alerts += " • " + alert + "\n"
            all_alerts += "\n"
        if len(list_alerts_oblast_title) == 0:
            all_alerts += f"Інші області :\n • Немає"
        else:
            all_alerts += f"Інші області :\n"
            for alert in list_alerts_oblast_title:
                all_alerts += " • " + alert + "\n"
    print(our_oblast)
    return all_alerts, our_oblast


async def wait_start_alarm():
    db = await Database.setup()

    text, is_active = await alert_func()
    if not is_active:
        return

    scheduler.remove_job("wait_start_alarm")
    scheduler.add_job(wait_finish_alarm, "interval", seconds=20, id="wait_finish_alarm")

    all_user_ids = map(lambda e: e[0], await db.list_id_student_agreed_alert_sql())
    all_teach_ids = map(lambda e: e[0], await db.list_id_teacher_agreed_alert_sql())
    await asyncio.gather(
        *map(send_notification(is_active=is_active, who=False), all_user_ids)
    )
    await asyncio.gather(
        *map(send_notification(is_active=is_active, who=True), all_teach_ids)
    )


async def wait_finish_alarm():
    db = await Database.setup()

    text, is_active = await alert_func()
    if is_active:
        return

    scheduler.remove_job("wait_finish_alarm")
    scheduler.add_job(wait_start_alarm, "interval", seconds=20, id="wait_start_alarm")

    all_user_ids = map(lambda e: e[0], await db.list_id_student_agreed_alert_sql())
    all_teach_ids = map(lambda e: e[0], await db.list_id_teacher_agreed_alert_sql())
    await asyncio.gather(
        *map(send_notification(is_active=is_active, who=False), all_user_ids)
    )
    await asyncio.gather(
        *map(send_notification(is_active=is_active, who=True), all_teach_ids)
    )


def send_notification(is_active: bool, who: bool):
    async def wrapped(user_id: int):
        try:
            if not who:
                await bot.send_sticker(
                    user_id,
                    r"CAACAgIAAxkBAAEI_1hkY5y8yh_-0cKFPQ5Sv2SWlYQaCwACLCUAAvF3IUhe2e30dH6RaC8E"
                    if is_active
                    else r"CAACAgIAAxkBAAEI_1xkY5zsKG4_LdSX-d2oMY994WAHjQACQisAAssEIUhdsPeRZOOUMC8E",
                )

                await bot.send_message(
                    user_id, "Тривога! 🔴" if is_active else "Відбій! 🟢"
                )
            if who:
                await bot.send_message(
                    user_id, "Тривога! 🔴" if is_active else "Відбій! 🟢"
                )
        except:
            pass

    return wrapped


async def create_task_alarm():
    scheduler.add_job(wait_start_alarm, "interval", seconds=20, id="wait_start_alarm")
    scheduler.start()
