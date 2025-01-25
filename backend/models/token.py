import backend.models.base as base
import backend.models.user as user

from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import (Integer, 
                        Text, 
                        String, 
                        Boolean, 
                        DateTime, 
                        Date, 
                        ForeignKey, 
                        func)
from typing import Optional

class Token(base.BaseModel):
    __tablename__ = "user_tokens"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    reset_password_token: Mapped[str] = mapped_column(String(255), nullable=True)
    email_token: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    user: Mapped["user.User"] = relationship("User", backref="tokens", lazy="joined")

