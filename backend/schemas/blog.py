from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import date, datetime



class CreateBlog(BaseModel):
    title: str 
    slug: str 
    content: Optional[str] = None 
    
    @field_validator('title', 'slug', mode='before')
    @classmethod
    def generate_slug(cls, values):
        if 'title' in values:
            values['slug'] = values.get("title").replace(" ","-").lower()
        return values

        
class ShowBlog(BaseModel):
    title:str 
    content: Optional[str]
    created_at: date

    class Config():
        from_attributes = True
    
    @field_validator('created_at', mode='before')
    @classmethod
    def convert_dateime_to_date(cls, value):
        if isinstance(value, datetime):
            return value.date()
        return value