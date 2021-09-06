from quizapp.core.config import SECRET_KEY
from quizapp.services.jwt import get_email_from_token
from fastapi import APIRouter, Request, Body
from quizapp.models.quiz.Question import Question, QuestionInCreate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
router = APIRouter()


@router.get("/question/{question_id}")
async def get_question(request: Request, question_id: str):
    """
    Retrieve a question by id
    """
    question = await Question.objects.find_one({"_id": ObjectId(question_id)})
    if question is None:
        return JSONResponse(status_code=404, content={"message": "Question not found"})
    options = question.get("options")
    for index in range(len(options)):
        options[index] = await request.app.mongodb["option"].find_one({"_id": ObjectId(options[index])})

    return JSONResponse(question, status_code=200, content_type="application/json")


@router.post("/new_question/{quiz_id}")
async def Create_Question(request: Request, quiz_id: str, Question_details: QuestionInCreate = Body(...)):
    try:
        Question_details = jsonable_encoder(Question_details)
        token = request.headers.get("Authorization")
        if(token is None):
            return JSONResponse(status_code=401, content={"message": "Token is required."})
        user_email = get_email_from_token(token, str(SECRET_KEY))
        if(user_email is None):
            return JSONResponse(status_code=401, content={"message": "Not Authorized."})

        Question_details["created_by"] = user_email
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


@router.patch("/update_question/{question_id}")
async def update_Question(request: Request, question_id: str, Question_details: Question = Body(...)):
    try:
        token = request.headers.get("Authorization")
        if(token is None):
            return JSONResponse(status_code=401, content={"message": "Token is required."})
        user_email = get_email_from_token(token, str(SECRET_KEY))
        if(user_email is None):
            return JSONResponse(status_code=401, content={"message": "Not Authorized."})
        Question_details = Question_details.dict(exclude_unset=True)
        Question_details = jsonable_encoder(Question_details)
        await request.app.mongodb["question"].find_one_and_update(
            {"_id": ObjectId(question_id)},
            {'$set': Question_details, "$addToSet": {"edited_by": user_email}})
        return JSONResponse(Question_details, status_code=200)
    except:
        return JSONResponse(status_code=400)


@router.delete("/{question_id}")
async def delete_Question(request: Request, question_id: str):
    try:
        token = request.headers.get("Authorization")
        if(token is None):
            return JSONResponse(status_code=401, content={"message": "Token is required."})
        user_email = get_email_from_token(token, str(SECRET_KEY))
        if(user_email is None):
            return JSONResponse(status_code=401, content={"message": "Not Authorized."})
        question = await request.app.mongodb["question"].find_one({"_id": ObjectId(question_id)})
        if(question is None):
            return JSONResponse(status_code=404, content={"message": "Question not found."})
        quiz_id = question.get("quiz_id")
        quiz = await request.app.mongodb["quiz"].find_one({"_id": ObjectId(quiz_id)})
        if(quiz is None):
            return JSONResponse(status_code=404, content={"message": "Quiz not found."})
        if(quiz.get("author") != user_email or user_email not in quiz.get("editors")):
            return JSONResponse(status_code=401, content={"message": "Not Authorized."})
        await request.app.mongodb["quiz"].find_one_and_update(
            {"_id": ObjectId(quiz_id)},
            {'$pull': {
                "questions": question_id
            }})
        await request.app.mongodb["question"].delete_one({"_id": ObjectId(question_id)})
        options = question.get("options")
        for option in options:
            await request.app.mongodb["option"].delete_one({"_id": ObjectId(option)})
        return JSONResponse(status_code=200)
    except:
        return JSONResponse(status_code=400)
