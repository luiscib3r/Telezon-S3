import os
import tempfile

from app.core.config import CID
from app.storage import Storage
from app.storage.telegram.bot import bot


class TelegramBotStorage(Storage):
    async def put_file(self, file: bytes, filename: str) -> str:
        result = await bot.send_document(CID, file, filename=filename)
        return str(result.document.file_id)

    async def get_file(self, file_id: str):
        new_file = await bot.get_file(file_id)
        file_name = os.path.join(tempfile.gettempdir(), f"telezon_{file_id}")
        await new_file.download_to_drive(file_name)

        return open(file_name, "rb")
