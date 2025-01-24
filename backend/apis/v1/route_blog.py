from fastapi import APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

from backend.db.connection import get_connection
from backend.schemas.blog import ShowBlog, CreateBlog, UpdateBlog
from backend.crud.blog import get_blog_crud , BlogCRUD
from backend.models.base import User
from backend.utils.security import auth_serv
router = APIRouter()

@router.post("/blogs",response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
async def create_blog(
    body: CreateBlog, 
    user:User = Depends(auth_serv.get_current_user), 
    crud: BlogCRUD = Depends(get_blog_crud)):
    """create blog by curent user"""
    return await crud.create_new_blog(body, user)

@router.get('/blogs', response_model=list[ShowBlog])
async def list_the_blogs(
    user: User = Depends(auth_serv.get_current_user), 
    crud:BlogCRUD = Depends(get_blog_crud)):
    """get all blogs current user"""
    return  await crud.list_blogs(user)

@router.get('/blog/{id}', response_model=ShowBlog)
async def read_blog(
    id: int, 
    user:User = Depends(auth_serv.get_current_user),
    crud: BlogCRUD = Depends(get_blog_crud)):
    blog = await crud.retreive_blog(id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} does not exists'
        )
    return blog

@router.put('/blog/{id}', response_model=ShowBlog)
async def update_blog(
    id:int, 
    body:UpdateBlog, 
    user:User = Depends(auth_serv.get_current_user),
    crud: BlogCRUD = Depends(get_blog_crud)):
    blog = await crud.update_blog(id, body)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with id {id} does not found'
        )
    return blog

@router.delete('/del_blog/{id}')
async def delete_a_blog(
    id:int, 
    user:User = Depends(auth_serv.get_current_user),
    crud: BlogCRUD = Depends(get_blog_crud)):
    message = await crud.delete_blog(id, user)
    if message.get('error'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message.get('error')
        )
    return {'msg':f'Succesfullu deleted blog with id {id}'}



