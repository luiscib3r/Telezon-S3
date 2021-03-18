from abc import ABC


class Storage(ABC):
    def put_file(self, file, filename: str) -> str:
        pass

    def get_file(self, file_id: str):
        pass
