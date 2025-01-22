from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.schemas.user import UserCreate
from backend.models.base import User

from backend.db.connection import get_connection
from fastapi import Depends

async def create_new_user(body:UserCreate, db:AsyncSession = Depends(get_connection)):
    """
    создать нового пользователя в базе данных
    Args:
        body (UserCreate): тело запроса из данными
        db (AsyncSession, optional): коннект с бд. Defaults to Depends(get_connection).
    """
    new_user = User(
       email = body.email,
       password_hash = body.password_plain,
       is_active = True,
       is_superuser = False
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def if_exist_user(email:str, db:AsyncSession = Depends(get_connection))->bool:
    """проверка что такого пользователя нету в базу данных"""
    query = select(User).filter(User.email == email)
    result = await db.execute(query) #выполняем запрос
    user = result.scalar_one_or_none() #получаем рузультат
    return user is not None