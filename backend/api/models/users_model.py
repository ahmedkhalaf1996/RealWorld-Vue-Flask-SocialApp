from typing import List, Optional
from pydantic import Field,BaseModel

class User(BaseModel):
    name: str 
    email: str 
    password: str 
    bio:Optional[str] = Field(default="")
    imageUrl:Optional[str] = Field(default="")
    followers:Optional[list[str]] = Field(default=[])
    following:Optional[list[str]] = Field(default=[])