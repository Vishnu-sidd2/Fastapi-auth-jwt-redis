from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routers import auth_router

#life span of our application
@asynccontextmanager
async def life_span(app:FastAPI):
  print(f"Server is Starting ....")
  await init_db()
  yield #its like a barrier one run at start and other at end 
  print(f"Server Is Stopped ...")

version ="v1"

app = FastAPI(
  title='FastApi Backend',
  version=version,
  lifespan=life_span
)

app.include_router(book_router,prefix=f"/api/{version}/books")

app.include_router(auth_router,prefix=f"/api/{version}/auth" , tags=['auth'])



