from fastapi import Request, Response
from pydantic import EmailStr
from quizapp.models.users.User import UserInResponse


async def check_username_is_taken(request: Request, email: EmailStr) -> bool:
    """
    Check if the username is taken.
    """
    try:
        QueryResult = await request.app.mongodb['user'].find_one({"email": email})
        return bool(QueryResult)
    except Exception as e:
        return False


async def get_user_by_email(request: Request, email: EmailStr) -> UserInResponse:
    try:
        QueryResult = await request.app.mongodb['user'].find_one({"email": email})
        if QueryResult:
            return QueryResult
        else:
            raise Exception("User not found")
    except Exception as e:
        return None
