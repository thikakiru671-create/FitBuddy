# FitBuddy – AI Fitness Plan Generator

FitBuddy is an AI-powered fitness planning web application built with
FastAPI, SQLite, Jinja2, and Google Gemini models.

The application generates a personalized 7-day workout plan based on
the user's age, weight, fitness goal, workout intensity, and experience
level.

It also generates a nutrition/recovery tip and allows the user to
provide feedback and generate a revised workout plan.

---

## Features

- Personalized 7-day workout plan
- AI-powered workout generation
- Nutrition and recovery guidance
- User profile storage
- SQLite database
- Workout plan revision using user feedback
- Admin user view
- FastAPI backend
- Jinja2 HTML frontend
- Gemini API integration
- Mock AI mode for testing without an API key
- Automated application tests

---

## Project Structure

```text
FitBuddy/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── routes.py
│   ├── gemini_client.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   └── updated_plan.py
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── error.html
│   └── all_users.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── images/
│       └── fitness-bg.svg
│
├── tests/
│   └── test_app.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE