from fastapi import APIRouter, Request, Body
from quizapp.models.quiz.Quiz import Quiz
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
router = APIRouter()


@router.post("/create_quiz")
async def create_Quiz(request: Request, quiz_details: Quiz = Body(...)):
    quiz_details = jsonable_encoder(quiz_details)
    newQuiz = await request.app.mongodb["quiz"].insert_one(quiz_details)
    retrieveNewQuiz = await request.app.mongodb["quiz"].find_one({"_id": newQuiz.inserted_id})
    retrieveNewQuiz["_id"] = str(retrieveNewQuiz.get("_id"))
    author = await request.app.mongodb["user"].find_one_and_update(
        {"email": quiz_details.get("author")},
        {'$push': {"quizes_Owned": retrieveNewQuiz["_id"]}})
    return JSONResponse(retrieveNewQuiz, status_code=201)


@router.patch("/update_quiz")
async def update_Quiz(request: Request, quiz_details: Quiz = Body(...)):
    # to be written
    return True


@router.delete("/{quiz_id}")
async def delete_Quiz(request: Request, quiz_id: str):
    # to be written
    return True
