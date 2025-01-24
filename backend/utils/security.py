from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import pytz
from backend.utils.jwt_process import JWTService
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.connection import get_connection
from backend.crud.user import get_user
from backend.core.config import settings
from backend.models.base import User
from abc import ABC, abstractmethod


class ConstructionAuthService(ABC):

    @abstractmethod
    async def get_current_user(
        self, toke: str, db: AsyncSession
    ) -> Optional["User"]: ...


class AuthService(ConstructionAuthService):
    auth2scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    
    async def get_current_user(
        self,
        token: str = Depends(auth2scheme),
        db: AsyncSession = Depends(get_connection),
    ):

        credential_exeptions = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            email = await JWTService().decode_token(token, settings.access_token)
            if email is None:
                raise credential_exeptions
        except JWTError:
            raise credential_exeptions

        user = await get_user(email,  db)
        return user


auth_serv = AuthService()
