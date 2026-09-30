from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .database import init_db
from .routes import router


# ---------------------------------------------------------
# APPLICATION LIFESPAN
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create SQLite tables when application starts
    init_db()

    yield


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

settings = get_settings()


# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-powered personalized fitness plan generator "
        "using FastAPI, SQLite and Google Gemini."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------

static_directory = (
    Path(__file__).parent / "static"
)

app.mount(
    "/static",
    StaticFiles(
        directory=str(static_directory)
    ),
    name="static",
)


# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

app.include_router(router)


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
        "application": settings.app_name,
        "ai_mode": (
            "mock"
            if settings.mock_ai
            else "gemini"
        ),
    }