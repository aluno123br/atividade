from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes import health_router, profiles_router, projects_router, technologies_router
from app.core.config import get_settings
from app.core.exceptions import AppException
from app.database import Base, engine
import app.models  # noqa: F401

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    api = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    @api.exception_handler(AppException)
    async def app_exception_handler(_: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.message},
        )

    @api.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            location = ".".join(str(item) for item in error.get("loc", []) if item != "body")
            errors.append({"field": location or "request", "message": error.get("msg", "Valor inválido")})
        return JSONResponse(
            status_code=400,
            content={"status": 400, "message": "Dados inválidos", "errors": errors},
        )

    @api.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException):
        message = exc.detail if isinstance(exc.detail, str) else "Erro na requisição"
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": message},
        )

    @api.exception_handler(Exception)
    async def unexpected_exception_handler(_: Request, exc: Exception):
        detail = str(exc) if settings.debug else "Ocorreu um erro interno no servidor"
        return JSONResponse(status_code=500, content={"status": 500, "message": detail})

    api.include_router(health_router)
    api.include_router(profiles_router)
    api.include_router(technologies_router)
    api.include_router(projects_router)
    return api


app = create_app()
