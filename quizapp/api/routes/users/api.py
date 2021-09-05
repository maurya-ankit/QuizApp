from fastapi import APIRouter

from quizapp.api.routes.users import users

router = APIRouter()

router.include_router(users.router, prefix='/users')
