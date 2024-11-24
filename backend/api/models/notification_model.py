from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserInSchema(BaseModel):
    name: str 
    avatar: Optional[str] = None


class Notification(BaseModel):
    deatils:str 
    mainuid: str 
    targetid: str 
    isreded: bool = False
    createdAt : datetime = Field(default_factory=datetime.utcnow)
    user: UserInSchema