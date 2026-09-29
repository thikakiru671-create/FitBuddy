from pathlib import Path

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from app.gemini_generator import generate_workout_gemini

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "message": "FitBuddy AI is running"
    }


@router.post("/generate-workout")
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    experience_level: str = Form("beginner"),
):
    try:
        plan = generate_workout_gemini(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            experience_level=experience_level,
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "username": username,
                "user_id": user_id,
                "age": age,
                "weight": weight,
                "goal": goal,
                "intensity": intensity,
                "experience_level": experience_level,
                "plan": plan,
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "request": request,
                "error": str(e),
            }
        )