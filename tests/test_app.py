import os

os.environ["AI_MODE"] = "mock"

os.environ[
    "DATABASE_URL"
] = "sqlite:///./test_fitbuddy.db"

os.environ[
    "ADMIN_KEY"
] = "test-key"


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "FitBuddy" in response.text


def test_generate_workout_mock():

    response = client.post(
        "/generate-workout",
        data={
            "username": "Test User",
            "user_id": "TEST001",
            "age": "25",
            "weight": "70",
            "goal": "muscle gain",
            "intensity": "medium",
            "experience_level": "beginner",
        },
    )

    assert response.status_code == 200

    assert (
        "7-Day Workout Plan"
        in response.text
    )

    assert (
        "Nutrition"
        in response.text
    )