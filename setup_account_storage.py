# Run this file tu setup your telegram account storage
# Complete the authorization process
# More info https://docs.pyrogram.org/intro/setup.html

import os

from pyrogram import Client
from pyrogram.types import Message

from app.core.config import TELEGRAM_API_HASH, TELEGRAM_API_ID

if __name__ == "__main__":
    app = Client(
        "telegram",
        api_id=TELEGRAM_API_ID,
        api_hash=TELEGRAM_API_HASH,
        session_string=os.getenv("SESSION_STRING"),
        in_memory=True,
    )

    SESSION_STRING = ""

    with app:
        print("Save this in SESSION_STRING environment variable")
        print("SESSION_STRING\n")
        SESSION_STRING = app.export_session_string()
        print(SESSION_STRING)
        print("\n")

    client = Client(
        "telegram",
        api_id=TELEGRAM_API_ID,
        api_hash=TELEGRAM_API_HASH,
        session_string=SESSION_STRING,
        in_memory=True,
    )

    @client.on_message()
    def cid_handler(_: Client, message: Message):
        print(f"CHANNEL ID {message.chat.id}")

    print(
        "Send some text in your channel and save channel id in CID environment variable"
    )
    print("PRESS Ctrl^c to stop")
    client.run()
