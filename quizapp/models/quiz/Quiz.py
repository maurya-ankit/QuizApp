
from quizapp.models.Common import ObjectIdStr
from typing import Optional, Set, List, Dict
from pydantic import BaseModel, HttpUrl, EmailStr


class QuizInCreate(BaseModel):
    _id: ObjectIdStr = None
    name: str
    description: Optional[str]
    duration: Optional[str]
    from_: Optional[str]
    to_: Optional[str]
    image: Optional[HttpUrl] = None
    quiz_id: str
    questions: List[str] = []
    editors: List[EmailStr] = []
    user_access: List[EmailStr] = []
    is_private: bool = True
    randomness: bool = False


class Quiz(QuizInCreate):
    author: EmailStr
