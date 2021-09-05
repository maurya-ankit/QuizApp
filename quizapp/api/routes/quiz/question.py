from fastapi import APIRouter, Request, Body
from quizapp.models.quiz.Quiz import Question
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
router = APIRouter()


@router.post("/new_question/{quiz_id}")
async def Create_Question(request: Request, quiz_id: str, Question_details: Question = Body(...)):
    try:
        Question_details = jsonable_encoder(Question_details)
        newQuestion = await request.app.mongodb["question"].insert_one(Question_details)
        retrieveNewQuestion = await request.app.mongodb["question"].find_one({"_id": newQuestion.inserted_id})
        retrieveNewQuestion["_id"] = str(retrieveNewQuestion["_id"])
        quiz = await request.app.mongodb["quiz"].find_one_and_update(
            {"_id": ObjectId(quiz_id)},
            {'$push': {
                "questions": retrieveNewQuestion["_id"]
            }})
        return JSONResponse(retrieveNewQuestion, status_code=201)
    except:
        return JSONResponse(status_code=400)


@router.patch("/update_question")
async def update_Question(request: Request, Question_details: Question = Body(...)):
    # to be written
    return True


@router.delete("/{question_id}")
async def delete_Question(request: Request):
    # to be written
    return True
