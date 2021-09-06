from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from quizapp.api.errors.http_error import http_error_handler
from quizapp.api.errors.validation_error import http422_error_handler
from quizapp.api.routes.api import router as api_router
from quizapp.core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from quizapp.core.events import create_start_app_handler, create_stop_app_handler


from quizapp.core.config import DATABASE_URL, HOST, PORT, DEBUG


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler(
        "startup",
        create_start_app_handler(application))
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application))

    application.add_exception_handler(HTTPException,
                                      http_error_handler)
    application.add_exception_handler(
        RequestValidationError,
        http422_error_handler)

    application.include_router(api_router,
                               prefix=API_PREFIX)

    return application


app = get_application()


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run(
        "quizapp.main:app",
        host=HOST,
        reload=DEBUG,
        port=PORT,
    )


if __name__ == "__main__":
    start()
