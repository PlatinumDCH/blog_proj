from fastapi import APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from backend.db.connection import get_connection
from backend.schemas.blog import ShowBlog, CreateBlog
from backend.db.repository.blog import create_new_blog

router = APIRouter()

@router.post("/blogs",response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: CreateBlog, db: AsyncSession= Depends(get_connection)):
    new_blog = await create_new_blog(blog=blog,db=db,author_id=1)
    return new_blog