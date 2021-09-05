from fastapi import FastAPI
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from quizapp.core.config import DATABASE_URL, DATABASE_NAME


async def connect_to_db(app: FastAPI) -> None:
    logger.info("Connecting to {0}", repr(DATABASE_URL))

    app.mongodb_client = AsyncIOMotorClient(DATABASE_URL)
    app.mongodb = app.mongodb_client[DATABASE_NAME]

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    app.mongodb_client.close()

    logger.info("Connection closed")
