from pydantic import BaseModel

class NoteCreate(BaseModel):
    text: str

class NoteResponse(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True

class NoteUpdate(BaseModel):
    text: str

class UserCreate(BaseModel):
    name: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
