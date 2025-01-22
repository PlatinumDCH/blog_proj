from sqlalchemy.ext.asyncio import AsyncSession 
from backend.schemas.blog import CreateBlog
from backend.models.base import Blog
from sqlalchemy import select

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

