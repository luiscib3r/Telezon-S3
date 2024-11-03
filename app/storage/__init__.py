from app.storage.storage import Storage
from app.storage.telegram import (  # noqa: F401
    TelegramAccountStorage,
    TelegramBotStorage,
)

storage: Storage = TelegramBotStorage()
