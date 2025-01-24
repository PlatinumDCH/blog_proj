from typing import Optional
from pydantic import BaseModel, model_validator, field_validator
from datetime import date, datetime



class CreateBlog(BaseModel):
    title: str 
    slug: str 
    content: Optional[str] = None 
    
    @model_validator(mode='before')
    @classmethod
    def generate_slug(cls, values):
        if 'title' in values and not values.get('slug'):
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

class UpdateBlog(CreateBlog): ...
