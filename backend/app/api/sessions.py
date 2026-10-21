from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.sessions import (
    SessionCreateRequest,
    SessionCreateResponse,
    SessionResponse,
)
from app.services import mock_data
from app.services.mock_auth import get_current_user


router = APIRouter(
    prefix="/sessions",
    tags=["Workout Sessions"],
)


def check_session_access(session, current_user):
    if current_user["role"] == "admin":
        return True

    if current_user["role"] == "patient":
        return session["patient_id"] == current_user["id"]

    if current_user["role"] == "physiotherapist":
        for assignment in mock_data.ASSIGNMENTS:
            if (
                assignment["physiotherapist_id"] == current_user["id"]
                and assignment["patient_id"] == session["patient_id"]
                and assignment["status"] == "active"
            ):
                return True

    return False


@router.post("",response_model=SessionCreateResponse,status_code=201,)

async def create_session(request: SessionCreateRequest,current_user=Depends(get_current_user),):
    
    if current_user["role"] != "patient":
        raise HTTPException(
            status_code=403,
            detail="Only patients can create workout sessions",
        )

    if request.exercise_id not in mock_data.EXERCISES:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found",
        )

    now = datetime.now(timezone.utc)

    started_at = request.started_at or now
    completed_at = request.completed_at or now

    session_id = mock_data.NEXT_SESSION_ID
    mock_data.NEXT_SESSION_ID += 1

    result_id = mock_data.NEXT_RESULT_ID
    mock_data.NEXT_RESULT_ID += 1

    session = {
        "id": session_id,
        "patient_id": current_user["id"],
        "started_at": started_at,
        "completed_at": completed_at,
        "status": "completed",
        "notes": request.notes,
    }

    result = {
        "id": result_id,
        "session_id": session_id,
        "exercise_id": request.exercise_id,
        "repetitions": request.repetitions,
        "duration_seconds": request.duration_seconds,
        "score": request.score,
        "pain_level": request.pain_level,
        "notes": request.notes,
        "recorded_at": now,
    }

    mock_data.SESSIONS[session_id] = session
    mock_data.SESSION_RESULTS[result_id] = result

    created_session = mock_data.get_session(session_id)

    return {
        "message": "Session saved successfully",
        "session": created_session,
    }


@router.get("",response_model=list[SessionResponse],)

async def get_sessions(current_user=Depends(get_current_user),):

    sessions = []

    for session in mock_data.SESSIONS.values():
        if check_session_access(session, current_user):
            full_session = mock_data.get_session(session["id"])

            if full_session:
                sessions.append(full_session)

    sessions.sort(
        key=lambda session: session["started_at"],
        reverse=True,
    )

    return sessions


@router.get("/{session_id}",response_model=SessionResponse,)

async def get_session(session_id: int,current_user=Depends(get_current_user),):

    session = mock_data.SESSIONS.get(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    if not check_session_access(session, current_user):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to access this session",
        )

    full_session = mock_data.get_session(session_id)

    return full_session