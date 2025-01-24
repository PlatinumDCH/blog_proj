from sqlalchemy.ext.asyncio import AsyncSession 
from backend.schemas.blog import CreateBlog, UpdateBlog
from backend.models.base import Blog
from sqlalchemy import select
from backend.models.base import User
from fastapi import Depends
from backend.db.connection import get_connection
from abc import ABC, abstractmethod

class InstructionBlogCRUD(ABC):

    @abstractmethod
    async def create_new_blog(self, body, user): ...

    @abstractmethod
    async def retreive_blog(self, id): ...

    @abstractmethod
    async def list_blogs(self, user): ...

    @abstractmethod
    async def update_blog(self, id, user): ...

    @abstractmethod
    async def delete_blog(self, id, user): ...


class BlogCRUD(InstructionBlogCRUD):
    def __init__(self, db:AsyncSession):
        self.db: AsyncSession = db

    async def create_new_blog(self, blog: CreateBlog, user:User):
        """db operation from create blog by curent user"""
        new_blog = Blog(**blog.model_dump(), author_id=user.id)
        self.db.add(new_blog)
        await self.db.commit()
        await self.db.refresh(new_blog)
        return new_blog

    async def retreive_blog(self, id:int):
        """db operatuin, get select blog curent user"""
        result = await self.db.execute(select(Blog).filter(Blog.id == id))
        blog = result.scalar_one_or_none()
        return blog

    async def list_blogs(self, user: User):
        """db operatin, get all blogs curent user"""
        result = await self.db.execute(select(Blog).filter(Blog.author_id == user.id))
        blogs = result.scalars().all()
        return blogs

    async def update_blog(self, id:int, body: UpdateBlog):
        """db operation update select blog curent user"""
        result = await self.db.execute(select(Blog).filter(Blog.id == id))
        blog_in_db  = result.scalar_one_or_none()

        if not blog_in_db:
            return None
        
        blog_in_db.title = body.title
        blog_in_db.content = body.content
        self.db.add(blog_in_db)
        await self.db.commit()
        await self.db.refresh(blog_in_db)
        return blog_in_db

    async def delete_blog(self, id:int, user:User):
        """db operation, delete select blog by id"""
        result = await self.db.execute(select(Blog).filter(Blog.id == id))
        blog_in_id = result.scalar_one_or_none()
        if not blog_in_id:
            return {'error':f'Could not find blog with id {id}'}
        
        await self.db.delete(blog_in_id)
        await self.db.commit()

        return {'msg':f'delete blog with id {id}'}

async def get_blog_crud(db:AsyncSession = Depends(get_connection)):
    return BlogCRUD(db)

