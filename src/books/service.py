from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreatemodel,BookUpdatemodel
from sqlmodel import select,desc
from .models import Book
from datetime import datetime
import uuid

class BookService:
  async def get_all_books(self,session: AsyncSession):
    statement = select(Book).order_by(desc(Book.created_at))
    result = await session.exec(statement)
    return result.all()

#fetching a specified book 
  async def get_book(self,book_uid:str , session:AsyncSession):
     statement = select(Book).where(Book.uid == book_uid)
     
     result = await session.exec(statement)
  
     book= result.first()
     return book if book is not None else None 

#creating a book in db
  async def create_books(self,book_data,session:AsyncSession):
    
    new_book = Book(**book_data.dict())
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)  # Refresh to get UID and timestamps
    return new_book

#updating a book 
  async def update_books(self,book_uid,update_data:BookUpdatemodel , session:AsyncSession):
    
    book_to_update =  await self.get_all_books(book_uid,session)
    
    if book_to_update is not None:
       update_data_dict = update_data.model_dump()
    
       for k,v in update_data_dict.items():
        setattr(book_to_update,k,v)
      
        await session.commit()
      
        return book_to_update
    else:
      return None

#deleting a book 
  async def delete_books(self,book_uid:str , session:AsyncSession):
    
     book_to_delete = await self.get_all_books(book_uid,session)
     
     if book_to_delete is not None:
       await session.delete(book_to_delete)
       
       await session.commit()
       
       return {}
       
     else:
       return None
    
