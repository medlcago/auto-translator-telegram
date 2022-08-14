from telethon import TelegramClient

from data import config

api_id = config.api_id
api_hash = config.api_hash
client = TelegramClient("user_bot", config.api_id, config.api_hash).start()
