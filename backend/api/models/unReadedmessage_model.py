from pydantic import BaseModel

class UnReadedMsg(BaseModel):
    mainUserid: str 
    otherUserid: str 
    numOfUnreadedMessages: int  
    isReaded: bool 