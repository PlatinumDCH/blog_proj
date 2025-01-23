from fastapi import APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

from backend.db.connection import get_connection
from backend.schemas.blog import ShowBlog, CreateBlog, UpdateBlog
from backend.db.repository.blog import create_new_blog, retreive_blog, list_blogs
from backend.db.repository.blog import update_blog, delete_a_blog

router = APIRouter()

@router.post("/blogs",response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: CreateBlog, db: AsyncSession= Depends(get_connection)):
    new_blog = await create_new_blog(blog=blog,db=db,author_id=1)
    return new_blog

@router.get('/blogs', response_model=list[ShowBlog])
async def get_all_blogs(db: AsyncSession = Depends(get_connection)):
    """получить все записи пользователя"""
    blogs = await list_blogs(db)
    return blogs

@router.get('/blog/{id}', response_model=ShowBlog)
async def get_blog(id: int, db:AsyncSession = Depends(get_connection)):
    blog = await retreive_blog(id, db)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} does not exists'
        )
    return blog

@router.put('/blog/{id}', response_model=ShowBlog)
async def update_a_blog(id:int, body:UpdateBlog, db:AsyncSession = Depends(get_connection)):
    blog = await update_blog(id, body, db)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with id {id} does not found'
        )
    return blog

@router.delete('/delete/{id}')
async def delete_a_blog(id:int, db: AsyncSession = Depends(get_connection)):
    message = await delete_blog(id, db)
    if message.get('error'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message.get('error')
        )
    return {'msg':f'Succesfullu deleted blog with id {id}'}



