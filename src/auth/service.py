#logic with database , this file is repsobile for changes in our db creating nd all 

from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import UserCreateModel
from .utils import generate_hashed_password

class UserService:
  async def get_user_by_email(self,email:str,session:AsyncSession):
    statement = select(User).where(User.email == email)
    
    result = await session.exec(statement)
    
    user_by_email= result.first()
    return user_by_email
  
  async def user_exists(self,email,session:AsyncSession):
    
    user = await self.get_user_by_email(email,session)
    
    if user is not None:
      return True
    else:
      return False
    
  async def create_user(self,user_data:UserCreateModel,session:AsyncSession):
    
    user_data_dict=user_data.model_dump()
    
    new_user = User(
      **user_data_dict
    )
    
    new_user.password_hash = generate_hashed_password(user_data_dict['password'])
    
    session.add(new_user)
    
    await session.commit()
    
    return new_user