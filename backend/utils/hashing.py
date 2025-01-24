from passlib.context import CryptContext
import bcrypt
from dataclasses import dataclass


@dataclass
class SolveBugBryptWarning:
    __version__: str = getattr(bcrypt, "__version__")


setattr(bcrypt, "__about__", SolveBugBryptWarning())

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hesh(password):
        return pwd_context.hash(password)
