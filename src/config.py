import os

TOKEN = os.environ.get("BOT_TOKEN", "5999755878:AAG8GDhnLntBSK6ERJyHNPfNEI2wxUvhaSU")
SUPER_ADMIN = os.environ.get("SUPER_ADMIN", [2138964363, 862361179])
TOKEN_ALERT = os.environ.get(
    "TOKEN_ALERT", "8a7422052b4f13dd4497670ccfc776b4c2a04c7dab2203"
)
TOKEN_SENTRY = os.environ.get(
    "TOKEN_SENTRY",
    "https://622c27cfc84b46119192ff14073e2df9@o4504669478780928.ingest.sentry.io/4504669483827200",
)
KUMA_TOKEN = os.environ.get("KUMA_TOKEN", "")
