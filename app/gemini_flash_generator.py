from app.config import get_settings
from app.gemini_client import generate_text


def generate_nutrition_tip_with_flash(
    goal: str
) -> str:

    prompt = f"""
You are FitBuddy's nutrition and recovery assistant.

The user's fitness goal is:

{goal}

Provide ONE concise, practical
nutrition or recovery tip.

Use general wellness guidance.

Do not provide medical treatment
or extreme dieting advice.

Keep it to 2–4 sentences.
Make it actionable.
"""

    return generate_text(
        prompt,
        get_settings().fast_model
    )