from app.core.config import CID
from app.storage import Storage
from app.storage.telegram.bot import bot


class TelegramBotStorage(Storage):
    async def put_file(self, file: bytes, filename: str) -> str:
        result = await bot.send_document(CID, file, filename=filename)
        return str(result.document.file_id)

    async def get_file(self, file_id: str):
        file = await bot.get_file(file_id)
        return file
