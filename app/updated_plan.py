from app.config import get_settings
from app.gemini_client import generate_text


def update_workout_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str
) -> str:

    prompt = f"""
You are FitBuddy's plan revision assistant.

Goal: {goal}

Preferred intensity: {intensity}

Original 7-day plan:

---BEGIN PLAN---

{original_plan}

---END PLAN---

User feedback:

---BEGIN FEEDBACK---

{feedback}

---END FEEDBACK---

Create a revised 7-day plan.

Address the user's feedback while
preserving sensible training balance.

Keep at least one recovery/rest day.

Keep:

- Warm-up
- Main workout
- Cooldown/recovery

Do not make unsafe or extreme changes.

Return only the revised plan.

Use clear Day 1 through Day 7 headings.
"""

    return generate_text(
        prompt,
        get_settings().workout_model
    )