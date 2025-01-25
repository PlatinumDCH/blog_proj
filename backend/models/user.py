import backend.models.base as base
import backend.models.blog as blog

from sqlalchemy.orm import DeclarativeBase
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

class User(base.BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(150), nullable=False, unique=True, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    blogs: Mapped["blog.Blog"] = relationship("Blog", back_populates="author", lazy="joined")
    