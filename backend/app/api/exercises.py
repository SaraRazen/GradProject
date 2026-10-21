from fastapi import APIRouter, HTTPException

from app.schemas.exercises import ExerciseResponse
from app.services.mock_data import EXERCISES


router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"],
)


@router.get("",response_model=list[ExerciseResponse],)

async def get_exercises():
    return list(EXERCISES.values())


@router.get("/{exercise_id}",response_model=ExerciseResponse,)

async def get_exercise(exercise_id: int):
    exercise = EXERCISES.get(exercise_id)

    if exercise is None:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found",
        )

    return exercise