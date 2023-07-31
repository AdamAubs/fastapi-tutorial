from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


# Pydantic schema for the base properties of a post (used for validation and serialization)
class PostBase(BaseModel):
    title: str  # The title of the post (String)
    content: str  # The content/body of the post (string)
    published: bool = (
        True  # Whether the post is published (boolean); default value is True
    )


# Pydantice schema for creating a new post (inherits from PostBase)
class PostCreate(PostBase):
    pass  # No additional properties needed for creating a post; inherits properties from PostBase


# Pydantic schema for output to a new user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# Pydantic schema for reading/posting a post from/to the database (inherits from PostBase)
class Post(PostBase):
    id: int  # The id of the post
    created_at: datetime  # The time the post is published at is vaild (datetime)
    owner_id: int
    owner: UserOut

    # Configuration class for enabling from_attributes mode (ORM mode in Pydantic 2.x)
    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


# Pydantic schema for creating a new user to the database
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
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
