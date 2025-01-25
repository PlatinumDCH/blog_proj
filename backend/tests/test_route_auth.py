from unittest.mock import MagicMock, AsyncMock
from backend.models.base import User
from tests.conftest import TestingSessionLocal
from fastapi import status

import pytest
from sqlalchemy import select


user_data = {
        'email':'test@gmail.com',
        'password':'123',
    }


def test_create_user(client, monkeypatch):
    response = client.post("/signup",json=user_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "password" not in data