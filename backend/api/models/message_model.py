from pydantic import BaseModel

class Message(BaseModel):
    content: str 
    sender: str 
    recever: str 