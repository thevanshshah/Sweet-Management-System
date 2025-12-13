from typing import Optional
from sqlmodel import SQLModel, Field

class Sweet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    price: float
    quantity: int

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str

# Schema for receiving data (No ID, plain password)
class UserCreate(SQLModel):
    username: str
    password: str

# Schema for returning data (No password!)
class UserRead(SQLModel):
    id: int
    username: str