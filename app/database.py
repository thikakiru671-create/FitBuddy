from datetime import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)

from app.config import get_settings


settings = get_settings()

connect_args = {
    "check_same_thread": False
} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String(120)
    )

    age: Mapped[int] = mapped_column(
        Integer
    )

    weight: Mapped[float] = mapped_column()

    goal: Mapped[str] = mapped_column(
        String(80)
    )

    intensity: Mapped[str] = mapped_column(
        String(20)
    )

    experience_level: Mapped[str] = mapped_column(
        String(30),
        default="beginner"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Plan(Base):

    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[str] = mapped_column(
        String(80),
        index=True
    )

    original_plan: Mapped[str] = mapped_column(
        Text
    )

    updated_plan: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    nutrition_tip: Mapped[str] = mapped_column(
        Text
    )

    feedback: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )


def init_db() -> None:

    Base.metadata.create_all(
        bind=engine
    )


def save_user(
    user_id: str,
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
    experience_level: str = "beginner",
) -> User:

    with SessionLocal() as db:

        existing = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if existing:

            existing.username = username
            existing.age = age
            existing.weight = weight
            existing.goal = goal
            existing.intensity = intensity
            existing.experience_level = experience_level

            db.commit()
            db.refresh(existing)

            return existing

        user = User(
            user_id=user_id,
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            experience_level=experience_level,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user


def save_plan(
    user_id: str,
    original_plan: str,
    nutrition_tip: str,
) -> Plan:

    with SessionLocal() as db:

        plan = Plan(
            user_id=user_id,
            original_plan=original_plan,
            nutrition_tip=nutrition_tip,
        )

        db.add(plan)
        db.commit()
        db.refresh(plan)

        return plan


def get_user(
    user_id: str
) -> Optional[User]:

    with SessionLocal() as db:

        return (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )


def get_latest_plan(
    user_id: str
) -> Optional[Plan]:

    with SessionLocal() as db:

        return (
            db.query(Plan)
            .filter(Plan.user_id == user_id)
            .order_by(Plan.id.desc())
            .first()
        )


def get_original_plan(
    user_id: str
) -> Optional[str]:

    plan = get_latest_plan(user_id)

    return plan.original_plan if plan else None


def update_plan(
    user_id: str,
    updated_plan: str,
    feedback: str,
) -> Optional[Plan]:

    with SessionLocal() as db:

        plan = (
            db.query(Plan)
            .filter(Plan.user_id == user_id)
            .order_by(Plan.id.desc())
            .first()
        )

        if not plan:
            return None

        plan.updated_plan = updated_plan
        plan.feedback = feedback
        plan.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(plan)

        return plan


def get_all_users():

    with SessionLocal() as db:

        users = (
            db.query(User)
            .order_by(User.created_at.desc())
            .all()
        )

        output = []

        for user in users:

            plan = (
                db.query(Plan)
                .filter(
                    Plan.user_id == user.user_id
                )
                .order_by(Plan.id.desc())
                .first()
            )

            output.append(
                {
                    "user": user,
                    "plan": plan,
                }
            )

        return output