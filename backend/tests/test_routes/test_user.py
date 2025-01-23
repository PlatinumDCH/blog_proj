from unittest.mock import AsyncMock

user_data = {
        'email':'test@gmail.com',
        'password_plain':'1234',
    }

def test_create_user(client, monkeypatch):
    """успешная регистрация пользователя на сайте"""

    response = client.post("/signup",json=user_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == user_data["email"]
