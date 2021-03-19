import os
import tempfile

from app.storage import Storage
from app.storage.telegram.bot import bot
from app.core.config import CID


class TelegramBotStorage(Storage):
    def put_file(self, file, filename: str) -> str:
        result = bot.send_document(CID, file, filename=filename)
        return str(result.document.file_id)

    def get_file(self, file_id: str):
        new_file = bot.get_file(file_id)
        file_name = os.path.join(tempfile.gettempdir(), f'telezon_{file_id}')
        new_file.download(file_name)

        return open(file_name, 'rb')