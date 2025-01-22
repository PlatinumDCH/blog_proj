from sqlalchemy.ext.asyncio import AsyncSession 
from backend.schemas.blog import CreateBlog
from backend.models.base import Blog


async def create_new_blog(blog: CreateBlog, db: AsyncSession, author_id:int = 1):
    new_blog = Blog(
        **blog.model_dump(),
        author_id=author_id
        )
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog