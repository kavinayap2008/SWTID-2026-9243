from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    select,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    joinedload,
    mapped_column,
    relationship,
    sessionmaker,
)

from .config import get_settings


settings = get_settings()


# ---------------------------------------------------------
# DATABASE ENGINE
# ---------------------------------------------------------

connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# ---------------------------------------------------------
# BASE MODEL
# ---------------------------------------------------------

class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------
# USER MODEL
# ---------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    username: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    goal: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    intensity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    plan: Mapped["WorkoutPlan | None"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )


# ---------------------------------------------------------
# WORKOUT PLAN MODEL
# ---------------------------------------------------------

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    original_plan: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    updated_plan: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    last_feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    user: Mapped[User] = relationship(
        back_populates="plan",
    )


# ---------------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------------

def init_db() -> None:
    Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# SAVE / UPDATE USER
# ---------------------------------------------------------

def save_user(
    user_id: int,
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> User:

    with SessionLocal() as db:

        user = db.get(User, user_id)

        if user:
            user.username = username
            user.age = age
            user.weight = weight
            user.goal = goal
            user.intensity = intensity

        else:
            user = User(
                id=user_id,
                username=username,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
            )

            db.add(user)

        db.commit()
        db.refresh(user)

        return user


# ---------------------------------------------------------
# SAVE ORIGINAL PLAN
# ---------------------------------------------------------

def save_plan(
    user_id: int,
    plan: str,
) -> WorkoutPlan:

    with SessionLocal() as db:

        record = db.scalar(
            select(WorkoutPlan).where(
                WorkoutPlan.user_id == user_id
            )
        )

        if record:

            record.original_plan = plan
            record.updated_plan = None
            record.last_feedback = None

        else:

            record = WorkoutPlan(
                user_id=user_id,
                original_plan=plan,
            )

            db.add(record)

        db.commit()
        db.refresh(record)

        return record


# ---------------------------------------------------------
# UPDATE WORKOUT PLAN
# ---------------------------------------------------------

def update_plan(
    user_id: int,
    updated_text: str,
    feedback: str | None = None,
) -> WorkoutPlan | None:

    with SessionLocal() as db:

        record = db.scalar(
            select(WorkoutPlan).where(
                WorkoutPlan.user_id == user_id
            )
        )

        if not record:
            return None

        record.updated_plan = updated_text
        record.last_feedback = feedback

        db.commit()
        db.refresh(record)

        return record


# ---------------------------------------------------------
# GET ORIGINAL PLAN
# ---------------------------------------------------------

def get_original_plan(
    user_id: int,
) -> str | None:

    with SessionLocal() as db:

        record = db.scalar(
            select(WorkoutPlan).where(
                WorkoutPlan.user_id == user_id
            )
        )

        if record:
            return record.original_plan

        return None


# ---------------------------------------------------------
# GET ONE USER
# ---------------------------------------------------------

def get_user(
    user_id: int,
) -> User | None:

    with SessionLocal() as db:

        return db.scalar(
            select(User)
            .options(joinedload(User.plan))
            .where(User.id == user_id)
        )


# ---------------------------------------------------------
# GET ALL USERS
# ---------------------------------------------------------

def get_all_users() -> list[User]:

    with SessionLocal() as db:

        result = db.scalars(
            select(User)
            .options(joinedload(User.plan))
            .order_by(User.id)
        )

        return list(result.unique())


# ---------------------------------------------------------
# DELETE USER
# ---------------------------------------------------------

def delete_user(
    user_id: int,
) -> bool:

    with SessionLocal() as db:

        user = db.get(User, user_id)

        if not user:
            return False

        db.delete(user)
        db.commit()

        return True