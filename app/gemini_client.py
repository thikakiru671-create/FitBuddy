import time
from functools import lru_cache

from google import genai
from google.genai import types

from app.config import get_settings


class AIServiceError(RuntimeError):
    pass


@lru_cache
def get_client():

    settings = get_settings()

    if not settings.google_api_key:

        raise AIServiceError(
            "GOOGLE_API_KEY is not configured. "
            "Add it to .env or set AI_MODE=mock "
            "for local testing."
        )

    return genai.Client(
        api_key=settings.google_api_key
    )


def generate_text(
    prompt: str,
    model: str
) -> str:

    settings = get_settings()

    if settings.ai_mode.lower() == "mock":

        return mock_response(prompt)

    client = get_client()

    models_to_try = [model]

    if (
        settings.fallback_model
        and settings.fallback_model not in models_to_try
    ):
        models_to_try.append(
            settings.fallback_model
        )

    last_error = None

    for selected_model in models_to_try:

        for attempt in range(
            settings.ai_max_retries
        ):

            try:

                response = client.models.generate_content(
                    model=selected_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.6,
                        max_output_tokens=5000,
                    ),
                )

                text = (
                    response.text or ""
                ).strip()

                if not text:

                    raise AIServiceError(
                        "Gemini returned an empty response."
                    )

                return text

            except Exception as exc:

                last_error = exc

                if (
                    attempt
                    < settings.ai_max_retries - 1
                ):

                    time.sleep(
                        settings.ai_retry_delay_seconds
                        * (attempt + 1)
                    )

    raise AIServiceError(
        f"Gemini request failed after retries: "
        f"{last_error}"
    )


def mock_response(
    prompt: str
) -> str:

    lower = prompt.lower()

    if (
        "nutrition" in lower
        or "recovery" in lower
    ):

        return (
            "Prioritize regular hydration and include "
            "a protein-rich food in meals. After training, "
            "combine protein with a carbohydrate source and "
            "allow enough sleep and recovery between "
            "demanding sessions."
        )

    return """7-DAY FITBUDDY PLAN

Day 1 — Full Body
Warm-up: 7 minutes brisk walking and mobility.
Main: Bodyweight squats 3x10, push-ups 3x8,
glute bridges 3x12, plank 3x30 sec.
Cooldown: 5 minutes easy stretching.

Day 2 — Cardio
Warm-up: 5 minutes easy movement.
Main: 25 minutes moderate walking/cycling
with 5 x 1-minute faster intervals.
Cooldown: 5 minutes easy walking.

Day 3 — Recovery
Main: 20–30 minutes gentle walking plus mobility.
Recovery: Keep effort easy and focus on technique.

Day 4 — Upper Body + Core
Main: Incline push-ups 3x10, resistance-band rows
3x12, shoulder raises 2x12, dead bug 3x8/side.
Cooldown: 5 minutes stretching.

Day 5 — Lower Body
Main: Squats 3x10, reverse lunges 3x8/side,
hip hinges 3x10, calf raises 3x15.
Cooldown: 5 minutes easy stretching.

Day 6 — Cardio + Core
Main: 25 minutes easy-to-moderate cardio plus
bird-dog 3x8/side and plank 3x30 sec.
Cooldown: 5 minutes breathing and stretching.

Day 7 — Rest / Active Recovery
Take a rest day or do 20 minutes of comfortable
walking and gentle mobility.

Progression: Keep 1–3 comfortable repetitions in
reserve and increase volume gradually."""