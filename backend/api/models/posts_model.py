from typing import List, Optional
from pydantic import Field, BaseModel
from datetime import datetime


class Post(BaseModel):
    title: str 
    message: str 
    creator: str 
    selectedFile: str #img 
    name: str 
    likes: Optional[list[str]] = Field(default=[]) 
    comments: Optional[list[str]] = Field(default=[]) 
    createdAt: datetime = Field(default_factory=datetime.utcnow)




