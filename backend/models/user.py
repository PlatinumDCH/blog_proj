from models.base import BaseModel
from sqlalchemy import String
from models.base import BaseModel
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import Boolean

from .blog import Blog

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