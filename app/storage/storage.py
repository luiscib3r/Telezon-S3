from abc import ABC


class Storage(ABC):
    async def put_file(self, file: bytes, filename: str) -> str:
        pass

    async def get_file(self, file_id: str):
        pass
