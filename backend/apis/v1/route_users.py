from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from backend.schemas.user import UserCreate, ShowUser
from backend.db.connection import get_connection
from backend.crud.user import create_new_user, if_exist_user, autenticate_user
from backend.core.hashing import Hasher
from backend.schemas.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from backend.utils.jwt_process import jwt_serv

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

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  
    db: AsyncSession= Depends(get_connection)):
    user = await autenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    encode_access_token = await jwt_serv.create_access_token(
        data={"sub": user.email}
    )
    encode_refresh_token = await jwt_serv.create_refresh_token(
        data={'sub': user.email}
    )

    return {
        "access_token": encode_access_token, 
        "refresh_token": encode_refresh_token,
        "token_type": "bearer"}

