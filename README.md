# KOTEKBOT

[![Support Ukraine](https://badgen.net/badge/support/UKRAINE/?color=0057B8&labelColor=FFD700)](https://www.gov.uk/government/news/ukraine-what-you-can-do-to-help)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python support versions badge](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/)
[![Deploy](https://github.com/salko-ua/KOTEKBOT/actions/workflows/deploy.yml/badge.svg)](https://github.com/salko-ua/KOTEKBOT/actions/workflows/deploy.yml)

Bot created by [salko-ua](https://t.me/salkooua) for [my college](https://vvpc.com.ua/).

# Instalation

1. Get a token from [@BotFather in Telegram](https://t.me/BotFather)

2. Clone the repository (using the green button on the upper right) and install dependencies with `poetry install`

3. Make your changes to the bot and [create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)

## Database

Example usage database in the bot:
```python
from src.data_base import Database

# in any function
async def any_functon():
    db = await Database.setup() # initialization
    if await db.admin_exists(user_id):
        ... # code
```

You can check if something exists by user_id

- [Function exist in this file](src/data_base/exists.py)
- [Function add in this file](src/data_base/adds.py)
- [Function delete in this file](src/data_base/deletes.py)
- [Function select in this file](src/data_base/selects.py)
- [Function update in this file](src/data_base/updates.py)

## Utils

- All utils write in `utils.py` (Functions that have frequent use)
- Do not write single-use functions there
- path to [utils.py](src/utils.py) write right

## Keyboards 

You can check all keyboards:

- [Folder with keyboards](src/keyboards)
