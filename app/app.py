from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import Settings, settings
from app.database import init_db
from app.routers import api
from app.utils.logger import logger_setup
from app.utils.seed import create_admin

logger = logger_setup(__name__)


@asynccontextmanager
async def life_span(app: FastAPI):
    app.state.async_session = init_db()
    create_admin()
    logger.info("startup: triggered")

    yield
    await app.state.async_session.session.close()
    await app.state.async_session.session.engine.dispose()
    logger.info("shutdown: triggered")


def create_app(setting: Settings):

    app = FastAPI(
        title=setting.PROJECT_NAME,
        version=setting.VERSION,
        docs_url="/",
        redoc_url='/docs',
        description=setting.DESCRIPTION,
        lifespan=life_span,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api, prefix=settings.API_V1_STR)

    return app
