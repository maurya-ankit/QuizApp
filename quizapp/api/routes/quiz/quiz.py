from fastapi import APIRouter, Request, Body, Depends
from quizapp.models.quiz.Quiz import QuizInCreate, Quiz
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from quizapp.services.jwt import get_email_from_token
from quizapp.core.config import SECRET_KEY
router = APIRouter()


@router.get("/{id}", response_model=Quiz)
async def get_quiz(request: Request, id: str):
    try:
        if id is None:
            return JSONResponse(status_code=400, content={"message": "Id is required."})

        auth_token = request.headers.get("Authorization")
        user_email = get_email_from_token(auth_token, str(SECRET_KEY))
        if user_email is None:
            return JSONResponse(status_code=401, content={"message": "Invalid token."})
        """Get a quiz by id"""

        quiz = await request.app.mongodb["quiz"].find_one({"_id": ObjectId(id), "author": user_email})
        if quiz is None:
            return JSONResponse(status_code=404, content={"message": "Quiz not found."})
        quiz["_id"] = str(quiz["_id"])
        questions = quiz.get("questions")
        if questions is not None:
            for qindex in range(len(questions)):
                questions[qindex] = await request.app.mongodb["question"].find_one({"_id": ObjectId(questions[qindex])})
                questions[qindex]["_id"] = str(questions[qindex]["_id"])
                options = questions[qindex].get("options")
                if options is not None:
                    for oindex in range(len(options)):
                        options[oindex] = await request.app.mongodb["option"].find_one({"_id": ObjectId(options[oindex])})
                        options[oindex]["_id"] = str(options[oindex]["_id"])

        return JSONResponse(quiz, status_code=200)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post("/create_quiz")
async def create_Quiz(request: Request, quiz_details: QuizInCreate = Body(...)):
    try:
        quiz_details = jsonable_encoder(quiz_details)
        token = request.headers.get("Authorization")
        if(token is None):
            return JSONResponse(status_code=401, content={"message": "Token is required."})
        user_email = get_email_from_token(token, str(SECRET_KEY))
        if(user_email is None):
            return JSONResponse(status_code=401, content={"message": "Not Authorized."})
        quiz_details["author"] = user_email
        newQuiz = await request.app.mongodb["quiz"].insert_one(quiz_details)
        retrieveNewQuiz = await request.app.mongodb["quiz"].find_one({"_id": newQuiz.inserted_id})
        retrieveNewQuiz["_id"] = str(retrieveNewQuiz.get("_id"))
        author = await request.app.mongodb["user"].find_one_and_update(
            {"email": quiz_details.get("author")},
            {'$push': {"quizes_Owned": retrieveNewQuiz["_id"]}})
        return JSONResponse(retrieveNewQuiz, status_code=201)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.patch("/update_quiz/{quiz_id}")
async def update_Quiz(request: Request, quiz_id: str, quiz_details: QuizInCreate = Body(...)):
    try:
        token = request.headers.get("Authorization")
        if(token is None):
            return JSONResponse(status_code=401, content={"message": "Token is required."})
        user_email = get_email_from_token(token, str(SECRET_KEY))
        if(user_email is None):
            return JSONResponse(status_code=401, content={"message": "Not Authorized."})
        quiz_details = quiz_details.dict(exclude_unset=True)
        quiz_details = jsonable_encoder(quiz_details)
        await request.app.mongodb["quiz"].update_one({"_id": ObjectId(quiz_id), "author": user_email}, {"$set": quiz_details})
        return JSONResponse({"status": "quiz updated"}, status_code=200)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.delete("/{quiz_id}")
async def delete_Quiz(request: Request, quiz_id: str):
    try:
        token = request.headers.get("Authorization")
        if(token is None):
            return JSONResponse(status_code=401, content={"message": "Token is required."})
        user_email = get_email_from_token(token, str(SECRET_KEY))
        if(user_email is None):
            return JSONResponse(status_code=401, content={"message": "Not Authorized."})
        quiz = await request.app.mongodb["quiz"].find_one({"_id": ObjectId(quiz_id), "author": user_email})
        if quiz is None:
            return JSONResponse(status_code=404, content={"message": "Quiz not found."})
        await request.app.mongodb["quiz"].delete_one({"_id": ObjectId(quiz_id)})
        questions = quiz.get("questions")
        if questions is not None:
            for qindex in range(len(questions)):
                question = await request.app.mongodb["question"].find_one({"_id": ObjectId(questions[qindex])})
                options = question.get("options")
                if options is not None:
                    for oindex in range(len(options)):
                        await request.app.mongodb["option"].delete_one({"_id": ObjectId(options[oindex])})
                await request.app.mongodb["question"].delete_one({"_id": ObjectId(questions[qindex])})
        return JSONResponse({"status": "quiz deleted"}, status_code=200)

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
