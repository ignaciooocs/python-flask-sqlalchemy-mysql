from typing import Optional
from pydantic import BaseModel

class CreateUser(BaseModel):
  id: Optional[int] = None
  name: str
  email: str
  password: str

class UpdateName(BaseModel):
  name:str

class UpdateEmail(BaseModel):
  email:str

class UpdatePassword(BaseModel):
  password:str
  new_password:str