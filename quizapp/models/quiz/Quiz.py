
from quizapp.models.Common import ObjectIdStr
from typing import Optional, Set, List, Dict
from pydantic import BaseModel, HttpUrl, EmailStr


class Option(BaseModel):
    _id: ObjectIdStr = None
    ans_text: Optional[str]
    ans_image: Optional[HttpUrl] = None


class Question(BaseModel):
    _id: ObjectIdStr = None
    order: int = -1
    question_text: str
    question_description: Optional[str]
    image: Optional[HttpUrl] = None
    type_: str
    options: List[str] = []


class Quiz(BaseModel):
    _id: ObjectIdStr = None
    name: str
    description: Optional[str]
    duration: Optional[str]
    from_: Optional[str]
    to_: Optional[str]
    image: Optional[HttpUrl] = None
    questions: List[str] = []
    author: EmailStr
    editors: List[EmailStr] = []
    user_access: List[EmailStr] = []
    is_private: bool = True
    randomness: bool = False
