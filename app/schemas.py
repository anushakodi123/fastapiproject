from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class Post(PostBase):
    id: int
    created_at : datetime
    user_id: int
    user: UserOut

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostWithVotes(BaseModel):
    Post: Post
    votes: int