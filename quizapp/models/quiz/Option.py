from quizapp.models.Common import ObjectIdStr
from typing import Optional, Set, List, Dict
from pydantic import BaseModel, HttpUrl, EmailStr


class OptionInCreate(BaseModel):
    _id: ObjectIdStr = None
    option_text: Optional[str]
    option_image: Optional[HttpUrl] = None


class Option(OptionInCreate):
    question_id: str
