from datetime import datetime

from pydantic import BaseModel, Field


class SessionCreateRequest(BaseModel):
    exercise_id: int

    repetitions: int = Field(ge=0)

    duration_seconds: int = Field(ge=0)

    score: float = Field(ge=0, le=100)

    pain_level: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )

    notes: str | None = None

    started_at: datetime | None = None

    completed_at: datetime | None = None


class SessionResultResponse(BaseModel):
    id: int
    exercise_id: int
    exercise_name: str
    repetitions: int | None = None
    duration_seconds: int | None = None
    score: float | None = None
    pain_level: int | None = None
    notes: str | None = None
    recorded_at: datetime


class SessionResponse(BaseModel):
    id: int
    patient_id: int
    started_at: datetime
    completed_at: datetime | None = None
    status: str
    notes: str | None = None
    results: list[SessionResultResponse]


class SessionCreateResponse(BaseModel):
    message: str
    session: SessionResponse