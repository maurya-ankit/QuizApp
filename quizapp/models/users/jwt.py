from datetime import datetime

from pydantic import BaseModel, EmailStr


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class JWTUser(BaseModel):
    email: EmailStr
