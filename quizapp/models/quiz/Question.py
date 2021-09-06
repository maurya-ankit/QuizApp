from quizapp.models.Common import ObjectIdStr
from typing import Optional, Set, List, Dict
from pydantic import BaseModel, HttpUrl, EmailStr


class QuestionInCreate(BaseModel):
    _id: ObjectIdStr = None
    order: int = -1
    question_text: str
    question_description: Optional[str]
    image: Optional[HttpUrl] = None
    type_: str
    options: List[str] = []
    edited_by: Optional[List[EmailStr]] = []


class Question(QuestionInCreate):
    created_by: Optional[EmailStr] = None
