import os
import tempfile

from pyrogram import Client

from app.core.config import CID, SESSION_STRING, TELEGRAM_API_HASH, TELEGRAM_API_ID
from app.storage import Storage


class TelegramAccountStorage(Storage):
    async def put_file(self, file: bytes, filename: str) -> str:
        file_name = os.path.join(tempfile.gettempdir(), f"telezon_{filename}")

        with open(file_name, "wb") as f:
            f.write(file)

        async with Client(SESSION_STRING, TELEGRAM_API_ID, TELEGRAM_API_HASH) as app:
            result = await app.send_document(int(CID), file_name, file_name=filename)

            return str(result.document.file_id)

    async def get_file(self, file_id: str):
        file_name = os.path.join(tempfile.gettempdir(), f"telezon_{file_id}")

        async with Client(SESSION_STRING, TELEGRAM_API_ID, TELEGRAM_API_HASH) as app:
            await app.download_media(file_id, file_name)

            return open(file_name, "rb")
