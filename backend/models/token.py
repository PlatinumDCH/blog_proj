from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import Integer,String, ForeignKey
from typing import Optional
from models.base import BaseModel

from .user import User

class Token(BaseModel):
    __tablename__ = "user_tokens"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    reset_password_token: Mapped[str] = mapped_column(String(255), nullable=True)
    email_token: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship("Users", backref="tokens", lazy="joined")