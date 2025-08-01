from typing import Optional,List
from src.books.schemas import Bookmodel, BookUpdatemodel,BookCreatemodel
from fastapi import Header,HTTPException,status,Depends
from fastapi import APIRouter,status
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.books.models import Book
from src.auth.dependencies import AccessTokenBearer

book_router=APIRouter()
book_service =BookService()

access_token_bearer = AccessTokenBearer()


@book_router.get('/Greet') 
async def read_greetings(name:Optional[str] = "User" , age:int= 0)->dict: 
  return {"message": f"Greeting You {name} from Vishnu!", "age": age}


@book_router.get('/get_headers',status_code=200)
async def get_headers(
  accept:str = Header(None),
  content_type : str = Header(None),
  user_agent:str = Header(None),
  host:str = Header(None)
):
  req_headers={}
  req_headers['accept'] = accept
  req_headers['content_type'] = content_type
  req_headers['user_agent'] = user_agent
  req_headers['host'] = host
  return req_headers

# get all the books 
@book_router.get('/',response_model=List[Bookmodel])
async def get_books(session:AsyncSession =Depends(get_session),user_details =Depends(access_token_bearer)):
  books = await book_service.get_all_books(session)
  return books

#create a new book
@book_router.post('/create_books' , status_code=status.HTTP_201_CREATED,response_model=Bookmodel,
                  )
async def create_book(book_data:BookCreatemodel, session: AsyncSession = Depends(get_session),user_details = Depends(access_token_bearer))->dict:
  new_book = await book_service.create_books(book_data, session)
  return new_book

#data of specific book with id 
@book_router.get('/{book_uid}',response_model=Bookmodel)
async def get_book(book_uid:int,session: AsyncSession = Depends(get_session),user_details = Depends(access_token_bearer)):
  
  book = await book_service.get_book(book_uid,session)
  
  if book:
    return book
  else:
    raise HTTPException(status_code=404, detail="Book not found")


#updating the book data 
@book_router.patch('/{book_uid}')
async def update_book(book_uid:int,book_update_data:BookUpdatemodel,session: AsyncSession = Depends(get_session),user_details = Depends(access_token_bearer)):
  
  updated_book  = await book_service.update_books(book_uid,book_update_data,session)   
  
  if update_book:
    return updated_book
  else:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book Not Found")


#deleting the book
@book_router.delete('/{book_uid}',status_code=status.HTTP_202_ACCEPTED)
async def delete_book(book_uid:int,session: AsyncSession = Depends(get_session),user_details = Depends(access_token_bearer))->dict:
  
  book_to_delete=await book_service.delete_books(book_uid,session)
  
  if book_to_delete:
    return
  else:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
  
    