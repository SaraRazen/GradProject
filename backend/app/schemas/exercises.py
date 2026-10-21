from pydantic import BaseModel


class ExerciseResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    instructions: str | None = None
    difficulty: str | None = None
    is_active: bool