from fastapi import APIRouter
from quizapp.api.routes.users import api as auth_api

router = APIRouter()
router.include_router(auth_api.router, tags=["auth"], prefix="/auth")
