import bcrypt
from passlib.context import CryptContext

pws_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_salt() -> str:
    return bcrypt.gensalt().decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pws_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pws_context.hash(password)
