from sqlalchemy.ext.asyncio import AsyncSession 
from backend.schemas.blog import CreateBlog, UpdateBlog
from backend.models.base import Blog
from sqlalchemy import select
from typing import Optional

async def create_new_blog(blog: CreateBlog, db: AsyncSession, author_id:int = 1):
    new_blog = Blog(
        **blog.model_dump(),
        author_id=author_id
        )
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog

async def retreive_blog(id:int, db:AsyncSession):
    result = await db.execute(select(Blog).filter(Blog.id == id))
    blog = result.scalar_one_or_none()
    return blog


async def list_blogs(db:AsyncSession):
    result = await db.execute(select(Blog).filter(Blog.is_active==True))
    blogs = result.scalars().all()
    return blogs

async def update_blog(id:int, body: UpdateBlog, db: AsyncSession):
    result = await db.execute(select(Blog).filter(Blog.id == id))
    blog_in_db  = result.scalar_one_or_none()

    if not blog_in_db:
        return None
    
    blog_in_db.title = body.title
    blog_in_db.content = body.content
    db.add(blog_in_db)
    await db.commit()
    await db.refresh(blog_in_db)
    return blog_in_db

async def delete_blog(id:int, db:AsyncSession):
    result = await db.execute(select(Blog).filter(Blog.id == id))
    blog_in_id = result.scalar_one_or_none()
    if not blog_in_id:
        return {'error':f'Could not find blog with id {id}'}
    
    await db.delete(blog_in_id)
    await db.commit()

    return {'msg':f'delete blog with id {id}'}

