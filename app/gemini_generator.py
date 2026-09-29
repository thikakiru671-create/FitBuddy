from app.config import get_settings
from app.gemini_client import generate_text


SYSTEM_RULES = """
You are FitBuddy, a fitness-planning assistant.

Create practical, conservative,
beginner-friendly fitness guidance.

Do not diagnose medical conditions
or prescribe treatment.

If a user reports pain, injury,
pregnancy, a serious medical condition,
or another safety concern, recommend
professional medical guidance.
"""


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
    experience_level: str = "beginner",
) -> str:

    prompt = f"""
{SYSTEM_RULES}

Create a personalized 7-day workout plan for:

Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Preferred intensity: {intensity}
Experience: {experience_level}

Requirements:

- Exactly 7 days.
- Include warm-up.
- Include main workout.
- Include cooldown/recovery.
- Give exercises with sets/reps or duration.
- Give rest intervals.
- Include at least one recovery/rest day.
- Match the selected intensity.
- Avoid extreme calorie or weight-loss promises.
- Keep the output readable.
- Use Day 1 through Day 7 headings.
"""

    return generate_text(
        prompt,
        get_settings().workout_model
    )