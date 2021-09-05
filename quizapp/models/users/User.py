from typing import Optional, List
import uuid
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from quizapp.models.Common import ObjectIdStr


class UserId(BaseModel):
    _id: ObjectIdStr = None


class UserInLogin(UserId):
    email: EmailStr
    password: str


class UserInCreate(UserId):
    email: EmailStr
    password: str
    quizes_Owned: List[str] = []


class UserInUpdate(UserId):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None


class UserWithToken(UserId):
    email: EmailStr
    token: str


class UserInResponse(UserWithToken):
    id: str = Field(..., alias="_id")
    email: EmailStr
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None
    created_at: str
    updated_at: str
