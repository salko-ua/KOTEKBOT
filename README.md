# KOTEKBOT
[![Support Ukraine](https://badgen.net/badge/support/UKRAINE/?color=0057B8&labelColor=FFD700)](https://www.gov.uk/government/news/ukraine-what-you-can-do-to-help)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python support versions badge](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/)
[![DeepSource](https://deepsource.io/gh/PerchunPak/pinger-bot.svg/?label=active+issues&show_trend=true&token=Tast9YwlUsJbok_-qTQLL0vX)](https://deepsource.io/gh/PerchunPak/pinger-bot/?ref=repository-badge)

Bot created by [salko-ua](https://t.me/salkooua) for [collage](https://vvpc.com.ua/)

# Instalation

1.You must get token from @BotFather in telegram

2.Then clone repo and write in terminal ```poetry install```

3.Now you can make update after create pull request.

## 1.Database
Example usage database in the bot:
```python
from src.data_base import Database

# in any function
async def any_functon():
    db = await Database.setup() # initialization
    if await db.admin_exists(user_id):
        ... # code
```

You can check if something exists by id or user_id\
[Function exist in this file](src/data_base/exist.py)\
[Function add in this file](src/data_base/add.py)\
[Function delete in this file](src/data_base/delete.py)\
[Function select in this file](src/data_base/select.py)\
[Function update in this file](src/data_base/update.py)

## Utils
- All utils write only here (Functions that have frequent use)\
- Do not write single-use functions here