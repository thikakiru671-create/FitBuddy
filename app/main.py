from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import router
from app.database import init_db


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description="AI-powered 7-day workout and nutrition plan generator.",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)

app.include_router(router)


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health", tags=["system"])
def health():
    return {
        "status": "ok",
        "service": "fitbuddy"
    }