from pyrogram import Client
from os import getenv

API_ID = 7839236
API_HASH = "5c34945e1a52089f3bf434a44b25aa1d"
TOKEN = "6180070295:AAFjJSWRRDkLbwhDhpFq6o4wnK4E9GXV718"

UPDATES = "AxeBotz"
SUPPORT = "AxeChatz"
MUST_JOIN = UPDATES

asura = Client(
  "ASURA",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=TOKEN
)
print("[INFO]: STARTING BOT")
asura.start()

print("[INFO]: GATHERING INFO")
x = asura.get_me()
BOT_NAME = x.first_name
BOT_USERNAME = x.username
BOT_ID = x.id
