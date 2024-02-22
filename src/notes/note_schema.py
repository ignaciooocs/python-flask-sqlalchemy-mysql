from pydantic import BaseModel

class CreateNote(BaseModel):
  title: str
  content: str
  priority: bool = False

class UpdateTitle(BaseModel):
  title: str

class UpdateContent(BaseModel):
  content: str

class UpdatePriority(BaseModel):
  priority: bool