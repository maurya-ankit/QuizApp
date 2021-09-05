from fastapi import APIRouter
from quizapp.api.routes.users import users as auth_api
from quizapp.api.routes.quiz import quiz as quiz_api
from quizapp.api.routes.quiz import question as question_api
from quizapp.api.routes.quiz import option as option_api

router = APIRouter()
router.include_router(auth_api.router, tags=["auth"], prefix="/auth")
router.include_router(quiz_api.router, tags=["quiz"], prefix="/quiz")
router.include_router(question_api.router, tags=["question"], prefix="/quiz")
router.include_router(option_api.router, tags=["option"], prefix="/quiz")
