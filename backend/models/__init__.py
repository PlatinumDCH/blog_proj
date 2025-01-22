from .base import BaseModel
from .user import User
from .blog import Blog

__all__  = ["BaseModel", "User", "Blog"]

metadata = BaseModel.metadata
