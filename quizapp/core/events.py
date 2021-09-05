from typing import Callable

from fastapi import FastAPI

from loguru import logger

from quizapp.db.events import close_db_connection, connect_to_db


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        # pass
        await connect_to_db(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        # pass
        await close_db_connection(app)

    return stop_app
