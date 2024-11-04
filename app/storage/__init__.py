from app.storage.storage import Storage
from app.storage.telegram import (  # noqa: F401
    TelegramAccountStorage,
    TelegramBotStorage,
)

# You can use TelegramBotStorage or TelegramAccountStorage
# TelegramBotStorage uses telegram bot api through python-telegram-bot
# TelegramAccountStorage uses MTProto through pyrogram
storage: Storage = TelegramAccountStorage()
