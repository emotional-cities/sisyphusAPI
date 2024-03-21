import uvicorn

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

from app.config.config import configuration as cfg
from app.config.logging import create_logger
from app.routers import metadatapush, csvpush, dataset
from app.utils.app_exceptions import AppExceptionCase, app_exception_handler
from app.utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)


def create_app() -> FastAPI:

    app = FastAPI(title="sisyphus-api", root_path=cfg.ROOT_PATH)

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request, e):
        return await http_exception_handler(request, e)

    @app.exception_handler(RequestValidationError)
    async def custom_validation_exception_handler(request, e):
        return await request_validation_exception_handler(request, e)

    @app.exception_handler(AppExceptionCase)
    async def custom_app_exception_handler(request, e):
        return await app_exception_handler(request, e)

    sisyphusapi = FastAPI(title="Sisyphus API")

    sisyphusapi.include_router(metadatapush.router)
    sisyphusapi.include_router(csvpush.router)
    sisyphusapi.include_router(dataset.router)

    app.mount("/sisyphus/api/v1", sisyphusapi)

    app.logger = create_logger(name="app.main")

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, port=5000)
