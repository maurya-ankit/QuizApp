from fastapi import APIRouter, Request, Body
from quizapp.models.quiz.Quiz import Option
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
router = APIRouter()


@router.post("/new_option/{question_id}")
async def Create_Option(request: Request, question_id: str, Option_details: Option = Body(...)):
    try:
        Option_details = jsonable_encoder(Option_details)
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


@router.patch("/update_option")
async def update_Option(request: Request, Option_details: Option = Body(...)):
    # to be written
    return True


@router.delete("/{option_id}")
async def delete_Option(request: Request):
    # to be written
    return True
