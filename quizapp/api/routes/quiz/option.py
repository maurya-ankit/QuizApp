from fastapi import APIRouter, Request, Body
from quizapp.models.quiz.Option import OptionInCreate, Option
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
router = APIRouter()


@router.post("/new_option/{question_id}")
async def Create_Option(request: Request, question_id: str, Option_details: OptionInCreate = Body(...)):
    try:
        Option_details = jsonable_encoder(Option_details)
        Option_details["question_id"] = question_id
        newOption = await request.app.mongodb["answer"].insert_one(Option_details)
        retrieveNewOption = await request.app.mongodb["answer"].find_one({"_id": newOption.inserted_id})
        retrieveNewOption["_id"] = str(retrieveNewOption["_id"])
        question = await request.app.mongodb["question"].find_one_and_update(
            {"_id": ObjectId(question_id)},
            {"$push": {
                "options": retrieveNewOption["_id"]
            }})
        return JSONResponse(retrieveNewOption, status_code=201)

    except:
        return JSONResponse(status_code=400)


# @router.patch("/update_option")
# async def update_Option(request: Request, Option_details: Option = Body(...)):
#     # to be written
#     return True


@router.delete("/{quiz_id}/{question_id}/{option_id}")
async def delete_Option(request: Request, quiz_id: str, question_id: str, option_id: str):
    try:
        token = request.headers.get("Authorization")
        if(token is None):
            return JSONResponse(status_code=401, content={"message": "Token is required."})
        user_email = get_email_from_token(token, str(SECRET_KEY))
        if(user_email is None):
            return JSONResponse(status_code=401, content={"message": "Not Authorized."})
        quiz = await request.app.mongodb["quiz"].find_one({"_id": ObjectId(quiz_id)})
        if(quiz is None):
            return JSONResponse(status_code=404, content={"message": "Quiz not found."})
        if(user_email != quiz["author"] or user_email not in quiz["editors"]):
            return JSONResponse(status_code=401, content={"message": "Not Authorized."})
        question = await request.app.mongodb["question"].find_one({"_id": ObjectId(question_id)})
        if(question is None):
            return JSONResponse(status_code=404, content={"message": "Question not found."})
        option = await request.app.mongodb["option"].find_one({"_id": ObjectId(option_id)})
        if(option is None):
            return JSONResponse(status_code=404, content={"message": "Option not found."})
        if(option["question_id"] != question_id):
            return JSONResponse(status_code=400, content={"message": "Option not found."})
        await request.app.mongodb["option"].delete_one({"_id": ObjectId(option_id)})
        await request.app.mongodb["question"].find_one_and_update(
            {"_id": ObjectId(question_id)},
            {"$pull": {
                "options": option_id
            }})
        return JSONResponse(status_code=200)

    except:
        return JSONResponse(status_code=400)
