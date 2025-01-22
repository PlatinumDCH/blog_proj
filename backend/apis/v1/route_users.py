from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from backend.schemas.user import UserCreate, ShowUser
from backend.db.connection import get_connection
from backend.db.repository.user import create_new_user, if_exist_user
from backend.core.hashing import Hasher

router = APIRouter()

@router.post('/signup', response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_connection)):

    if await if_exist_user(body.email, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='accaunt already exists'
        )
    
    body.password_plain = Hasher.get_password_hesh(body.password_plain)
    new_user = await create_new_user(body, db)

    return new_user
