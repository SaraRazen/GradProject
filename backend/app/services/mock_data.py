from datetime import datetime, timedelta, timezone
import hashlib


# ---------------------------------------------------------
# PASSWORD HELPERS
# ---------------------------------------------------------

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


# ---------------------------------------------------------
# USERS
# ---------------------------------------------------------

USERS = {
    1: {
        "id": 1,
        "full_name": "Demo Patient",
        "email": "patient@example.test",
        "password_hash": hash_password("password123"),
        "role": "patient",
        "is_active": True,
    },
    2: {
        "id": 2,
        "full_name": "Demo Physiotherapist",
        "email": "physio@example.test",
        "password_hash": hash_password("password123"),
        "role": "physiotherapist",
        "is_active": True,
    },
    3: {
        "id": 3,
        "full_name": "Demo Administrator",
        "email": "admin@example.test",
        "password_hash": hash_password("password123"),
        "role": "admin",
        "is_active": True,
    },
}


# ---------------------------------------------------------
# MOCK ACCESS TOKENS
# ---------------------------------------------------------

TOKENS = {
    "mock-token-1": 1,
    "mock-token-2": 2,
    "mock-token-3": 3,
}


# ---------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------

EXERCISES = {
    1: {
        "id": 1,
        "name": "Knee Extension",
        "description": "A basic knee mobility exercise.",
        "instructions": "Sit upright and slowly straighten the knee.",
        "difficulty": "beginner",
        "is_active": True,
    },
    2: {
        "id": 2,
        "name": "Shoulder Raise",
        "description": "A controlled shoulder mobility exercise.",
        "instructions": "Raise the arm within a comfortable range.",
        "difficulty": "beginner",
        "is_active": True,
    },
}


# ---------------------------------------------------------
# DEMO SESSION DATA
# ---------------------------------------------------------

_now = datetime.now(timezone.utc)

SESSIONS = {
    1: {
        "id": 1,
        "patient_id": 1,
        "started_at": _now - timedelta(days=2, minutes=15),
        "completed_at": _now - timedelta(days=2),
        "status": "completed",
        "notes": "Fictional sample session",
    }
}


SESSION_RESULTS = {
    1: {
        "id": 1,
        "session_id": 1,
        "exercise_id": 1,
        "repetitions": 10,
        "duration_seconds": 90,
        "score": 85.0,
        "pain_level": 2,
        "notes": "Fictional sample result",
        "recorded_at": _now - timedelta(days=2),
    },
    2: {
        "id": 2,
        "session_id": 1,
        "exercise_id": 2,
        "repetitions": 8,
        "duration_seconds": 75,
        "score": 80.0,
        "pain_level": 1,
        "notes": "Fictional sample result",
        "recorded_at": _now - timedelta(days=2),
    },
}


# ---------------------------------------------------------
# DEMO ASSIGNMENT DATA
# ---------------------------------------------------------

ASSIGNMENTS = [
    {
        "physiotherapist_id": 2,
        "patient_id": 1,
        "status": "active",
    }
]


# ---------------------------------------------------------
# ID COUNTERS
# ---------------------------------------------------------

NEXT_USER_ID = 4
NEXT_SESSION_ID = 2
NEXT_RESULT_ID = 3


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def get_user_by_email(email: str):
    for user in USERS.values():
        if user["email"].lower() == email.lower():
            return user

    return None


def get_user_by_token(token: str):
    user_id = TOKENS.get(token)

    if user_id is None:
        return None

    return USERS.get(user_id)


def get_session_results(session_id: int):
    return [
        result
        for result in SESSION_RESULTS.values()
        if result["session_id"] == session_id
    ]


def get_session(session_id: int):
    session = SESSIONS.get(session_id)

    if session is None:
        return None

    results = []

    for result in get_session_results(session_id):
        result_copy = dict(result)

        exercise = EXERCISES.get(result["exercise_id"])

        result_copy["exercise_name"] = (
            exercise["name"]
            if exercise
            else "Unknown exercise"
        )

        results.append(result_copy)

    session_copy = dict(session)
    session_copy["results"] = results

    return session_copy