# creating pydantic models 

from pydantic import BaseModel,Field
from datetime import datetime
import uuid
from typing import List
from src.books.schemas import Bookmodel


class UserCreateModel(BaseModel):
  first_name : str = Field(max_length=30)
  last_name : str = Field(
    max_length=40
  )
  username:str = Field(
    max_length=10
  )
  email:str = Field(
    max_length=50
  )
  password:str = Field(
    min_length=5
  )
  
class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool 
    password_hash: str = Field(exclude=True)
    created_at: datetime 
    updated_at: datetime 
    books : List[Bookmodel]

class UserLoginModel(BaseModel):
  email:str = Field(
    max_length=50
  )
  password:str = Field(
    min_length=5
  )
  