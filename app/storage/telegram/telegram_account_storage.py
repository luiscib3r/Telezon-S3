import io

from pyrogram import Client

from app.core.config import CID, SESSION_STRING, TELEGRAM_API_HASH, TELEGRAM_API_ID
from app.storage import Storage


class TelegramAccountStorage(Storage):
    def client(self):
        return Client(
            "telegram",
            api_id=TELEGRAM_API_ID,
            api_hash=TELEGRAM_API_HASH,
            session_string=SESSION_STRING,
            in_memory=True,
        )

    async def put_file(self, file: bytes, filename: str) -> str:
        document = io.BytesIO(file)

        async with self.client() as app:
            async for _ in app.get_dialogs():
                pass
            response = await app.send_document(int(CID), document, file_name=filename)
            return str(response.document.file_id)

    async def get_file(self, file_id: str) -> io.BufferedReader:
        async with self.client() as app:
            file = await app.download_media(file_id, in_memory=True)
            file.seek(0)
            return file
