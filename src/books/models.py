from typing import Optional
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey,func
from sqlmodel import SQLModel, Field, Column,Relationship
from src.auth import models
# Ensure Column is imported

class Book(SQLModel, table=True):
    __tablename__ = "books" # Good practice to explicitly define table name
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), # Use as_uuid=True for native UUID type handling
            nullable=False,
            primary_key=True,
            server_default=func.gen_random_uuid()
        )
    )
    title: str
    author: str
    year: Optional[int] = None # Make optional if not always provided
    user_uid: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(UUID(as_uuid=True), ForeignKey("users.uid"), nullable=True)
    )
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True), 
            nullable=False, # Typically not nullable
            server_default=func.now()
        )
    )
    updated_at: datetime = Field( 
        sa_column=Column(
            pg.TIMESTAMP(timezone=True), 
            nullable=False,
            server_default=func.now(),  
            onupdate=func.now() 
        )
    )
    user:Optional['models.User'] = Relationship(back_populates="books")

    def __repr__(self):
        return f"<Book {self.title} (UID: {self.uid})>"