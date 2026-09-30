from typing import Literal

from pydantic import BaseModel, Field, field_validator


Intensity = Literal["low", "medium", "high"]


class UserInput(BaseModel):
    user_id: int = Field(gt=0)

    username: str = Field(
        min_length=2,
        max_length=80,
    )

    age: int = Field(
        ge=13,
        le=100,
    )

    weight: float = Field(
        gt=20,
        le=400,
    )

    goal: str = Field(
        min_length=3,
        max_length=200,
    )

    intensity: Intensity

    @field_validator("username", "goal")
    @classmethod
    def clean_text(cls, value: str) -> str:
        return " ".join(value.strip().split())


class FeedbackRequest(BaseModel):
    user_id: int = Field(gt=0)

    feedback: str = Field(
        min_length=3,
        max_length=1000,
    )

    @field_validator("feedback")
    @classmethod
    def clean_feedback(cls, value: str) -> str:
        return value.strip()