from typing import Optional
import uuid
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from bson import ObjectId


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise ValueError("Not a valid ObjectId")
        return str(v)


class UserId(BaseModel):
    _id: ObjectIdStr = None


class UserInLogin(UserId):
    email: EmailStr
    password: str


class UserInCreate(UserId):
    email: EmailStr
    password: str


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
