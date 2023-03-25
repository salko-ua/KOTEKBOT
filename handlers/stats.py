import datetime
from data_base.controller_db import add_or_update_stats, see_all_stats




async def stats_schedule_add(name, count):
    await add_or_update_stats(name, count)


async def stats_schedule_all_see():
    await see_all_stats()
