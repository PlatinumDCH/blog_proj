from sqlalchemy import Column, Integer, String
from models.base import BaseModel
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import Integer, Text, String, Boolean, DateTime, Date, ForeignKey, func
from typing import Optional

from .user import User

class Blog(BaseModel):
    __tablename__ = "blog"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    author: Mapped["User"] = relationship("User", back_populates="blogs", lazy="joined")
    created_at: Mapped[Date] = mapped_column(DateTime, default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
