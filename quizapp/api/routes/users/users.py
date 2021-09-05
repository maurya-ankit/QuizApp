from quizapp.models.users.User import UserInCreate, UserInResponse, UserInLogin
from fastapi import APIRouter, Request, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from quizapp.services.authentication import check_username_is_taken, get_user_by_email
from quizapp.services.jwt import create_access_token_for_user
from quizapp.core.config import SECRET_KEY
from quizapp.models.users.User import UserInResponse, UserWithToken
router = APIRouter()


@router.post("/register")
async def register(request: Request, user: UserInCreate = Body(...)):
    user = jsonable_encoder(user)
    if await check_username_is_taken(request, user["email"]):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "email already taken"})
    else:
        new_user = await request.app.mongodb["user"].insert_one(user)
        created_user = await request.app.mongodb["user"].find_one({"_id": new_user.inserted_id})
        token = create_access_token_for_user(created_user, str(SECRET_KEY))
        return UserWithToken(
            email=created_user.get("email"),
            bio=created_user.get("bio"),
            image=created_user.get("image"),
            token=token
        )


@router.post("/login")
async def login(request: Request, user_login: UserInLogin = Body(..., embed=True, alias="user")):
    wrong_login_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect login Information"
    )
    try:
        user = await get_user_by_email(request, user_login.email)
        if user and user.get("password") == str(user_login.password):
            token = create_access_token_for_user(user, str(SECRET_KEY))
            return UserWithToken(
                email=user.get("email"),
                bio=user.get("bio"),
                image=user.get("image"),
                token=token
            )
        else:
            raise wrong_login_error
    except Exception as e:
        raise wrong_login_error
