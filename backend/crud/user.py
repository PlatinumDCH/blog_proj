from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.schemas.user import UserCreate
from backend.models.base import User
from backend.utils.hashing import Hasher

from backend.db.connection import get_connection
from fastapi import Depends




async def create_new_user(body, db:AsyncSession):
    """
    create new user in db
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

async def if_exist_user(email:str, db: AsyncSession)->bool:
    """проверка что такого пользователя нету в базу данных"""
    query = select(User).filter(User.email == email)
    result = await db.execute(query) #выполняем запрос
    user = result.scalar_one_or_none() #получаем рузультат
    return user is not None



async def get_user(email:str,db: AsyncSession):
    """return user, user email"""
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    return user

async def autenticate_user(email:str, passord:str, db:AsyncSession):
    user = await get_user(email, db)
    if not user:
        return False
    if not Hasher.verify_password(passord, user.password_hash):
        return False
    return user
