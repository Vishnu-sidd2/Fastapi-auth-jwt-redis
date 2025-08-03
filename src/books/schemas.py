from pydantic import BaseModel
import uuid 
from datetime import datetime
from typing import Optional

class Bookmodel(BaseModel):
  uid:uuid.UUID
  title:str
  author:str
  year:int
  created_at : datetime
  updated_at : datetime
  
  class Config:
    orm_mode = True

class BookCreatemodel(BaseModel):
  title:str
  author:str
  year:int
  user_uid: Optional[uuid.UUID] = None 
  
  class Config:
    from_attributes=True


class BookUpdatemodel(BaseModel):
  title:str
  author:str