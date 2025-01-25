import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import asyncio
import pytest_asyncio

from backend.main import app
from backend.db.connection import get_connection
from backend.utils.hashing import Hasher
from backend.utils.jwt_process import jwt_serv
from backend.models.base import BaseModel, User

#======================================================================
#connection do database for testing
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine( # "car engine"
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass=StaticPool # one tread working
)
#======================================================================
#createing TestUser
test_user = {
    "email":"test@gmail.com",
    "password":"1234"
            }
#======================================================================
#create testing sessia
#fabric async sessia-sqlalchemy bind to testing database
TestingSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
    )
#==========================================================================
# initialization model and data in database every time before separate test
@pytest.fixture(scope="module", autouse=True)
def init_models_wrap():
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
            await conn.run_sync(BaseModel.metadata.create_all)
        async with TestingSessionLocal() as session:
            hash_password = Hasher.get_password_hash(
                test_user.get('password')
                )
            current_user = User(
                                email=test_user.get("email"), 
                                password=hash_password,
                                )
            session.add(current_user)
            await session.commit()

    asyncio.run(
        init_models()
        )
#======================================================================
# testing client fastapi
@pytest.fixture(scope="module")
def client():
    async def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        except Exception as err:
            
            await session.rollback()
            raise #повторно выбрасить исключение
        finally:
            await session.close()

    app.dependency_overrides[get_connection] = override_get_db

    yield TestClient(app)
#======================================================================
# generate token 
@pytest_asyncio.fixture()
async def get_token():
    token = await jwt_serv.create_access_token(
        data={
            "sub": test_user.ger("email")
            }
            )
    return token
