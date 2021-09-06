import logging
import sys
from typing import List
from loguru import logger
from starlette.config import Config

from starlette.datastructures import CommaSeparatedStrings, Secret

from quizapp.core.logging import InterceptHandler

API_PREFIX = "/api"

JWT_TOKEN_PREFIX = "Token"

VERSION = "0.0.0"

config = Config(".env")

HOST = config("HOST", cast=str, default="0.0.0.0")
PORT = config("PORT", cast=int, default=8000)

JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")

DEBUG: bool = config(
    "DEBUG",
    cast=bool,
    default=False)

DATABASE_URL: str = config(
    "DATABASE_URL",
    cast=str,
)

DATABASE_NAME: str = config(
    "DATABASE_NAME",
    cast=str,
    default="quizapp")

MAX_CONNECTIONS_COUNT: int = config(
    "MAX_CONNECTIONS_COUNT",
    cast=int,
    default=10)
MIN_CONNECTIONS_COUNT: int = config(
    "MIN_CONNECTIONS_COUNT",
    cast=int,
    default=10)

SECRET_KEY: Secret = config(
    "SECRET_KEY",
    cast=Secret)

PROJECT_NAME: str = config(
    "PROJECT_NAME",
    default="QuizApp")

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default=""
)

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = (
    "uvicorn.asgi",
    "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
