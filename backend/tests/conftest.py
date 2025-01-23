import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
import asyncio
from backend.main import app
from backend.db.connection import get_connection
from backend.models.other import BaseModel, User

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass=StaticPool

)
test_user = {
    "username": "test", 
    "email": "deadpool@example.com", 
    "password": "123",
    }

TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

@pytest.fixture(scope="module", autouse=True)
def init_models_wrap():
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
            await conn.run_sync(BaseModel.metadata.create_all)
        

    asyncio.run(init_models())

@pytest.fixture(scope="module")
def client():
    # Dependency override

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


@pytest.fixture
def mock_password_service(monkeypatch):
    # Замокировать метод get_password_hash
    def mock_get_password_hash(password):
        return "mocked_hashed_password"
    monkeypatch.setattr("app.services.base.service.password.get_password_hash", mock_get_password_hash)
