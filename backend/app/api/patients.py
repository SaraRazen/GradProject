from fastapi import APIRouter, Depends, HTTPException

from app.schemas.patients import PatientResponse
from app.schemas.sessions import SessionResponse
from app.services import mock_data
from app.services.mock_auth import get_current_user


router = APIRouter(prefix="/patients",tags=["Patients"],)


def is_assigned_physio(physiotherapist_id: int, patient_id: int):
    for assignment in mock_data.ASSIGNMENTS:
        if (
            assignment["physiotherapist_id"] == physiotherapist_id
            and assignment["patient_id"] == patient_id
            and assignment["status"] == "active"
        ):
            return True

    return False


def can_view_patient(current_user, patient_id: int):
    if current_user["role"] == "admin":
        return True

    if current_user["role"] == "patient":
        return current_user["id"] == patient_id

    if current_user["role"] == "physiotherapist":
        return is_assigned_physio(
            current_user["id"],
            patient_id,
        )

    return False


@router.get("",response_model=list[PatientResponse],)

async def get_patients(
    current_user=Depends(get_current_user),
):
    if current_user["role"] not in {"physiotherapist", "admin"}:
        raise HTTPException(
            status_code=403,
            detail="Only physiotherapists and administrators can list patients",
        )

    patients = []

    for user in mock_data.USERS.values():
        if user["role"] != "patient":
            continue

        if current_user["role"] == "admin":
            patients.append(user)

        elif is_assigned_physio(
            current_user["id"],
            user["id"],
        ):
            patients.append(user)

    return patients


@router.get("/{patient_id}",response_model=PatientResponse,)

async def get_patient(
    patient_id: int,
    current_user=Depends(get_current_user),
):
    patient = mock_data.USERS.get(patient_id)

    if patient is None or patient["role"] != "patient":
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    if not can_view_patient(current_user, patient_id):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to access this patient",
        )

    return patient


@router.get("/{patient_id}/sessions",response_model=list[SessionResponse],)

async def get_patient_sessions(
    patient_id: int,
    current_user=Depends(get_current_user),
):
    patient = mock_data.USERS.get(patient_id)

    if patient is None or patient["role"] != "patient":
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    if not can_view_patient(current_user, patient_id):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to access this patient's sessions",
        )

    sessions = []

    for session in mock_data.SESSIONS.values():
        if session["patient_id"] != patient_id:
            continue

        full_session = mock_data.get_session(session["id"])

        if full_session:
            sessions.append(full_session)

    sessions.sort(
        key=lambda session: session["started_at"],
        reverse=True,
    )

    return sessions