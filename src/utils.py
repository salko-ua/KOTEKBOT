from datetime import datetime
from translate import Translator


async def get_current_date() -> str:
    translator = Translator(to_lang="uk")
    now = datetime.now()
    now = now.strftime("%d - %B, %A")
    return translator.translate(now)
