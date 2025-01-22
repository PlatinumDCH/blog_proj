from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password_plain: str = Field(..., min_length=4)

class ShowUser(BaseModel):
    id:int
    email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config():
        from_attributes = True
    
