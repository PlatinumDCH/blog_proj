from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import Integer, Text, String, Boolean, DateTime, Date, ForeignKey, func
from typing import Optional

class BaseModel(DeclarativeBase): ...


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


class User(BaseModel):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(150), nullable=False, unique=True, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    blogs: Mapped["Blog"] = relationship("Blog", back_populates="author", lazy="joined")
