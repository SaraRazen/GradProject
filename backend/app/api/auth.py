from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserResponse,
)
from app.services.mock_auth import get_current_user
from app.services import mock_data


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def public_user(user: dict) -> dict:
    """
    Return user information without exposing the password hash.
    """
    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "role": user["role"],
        "is_active": user["is_active"],
    }


@router.post("/register",response_model=AuthResponse,status_code=status.HTTP_201_CREATED,)

async def register(request: RegisterRequest):
    existing_user = mock_data.get_user_by_email(request.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    user_id = mock_data.NEXT_USER_ID
    mock_data.NEXT_USER_ID += 1

    user = {
        "id": user_id,
        "full_name": request.full_name,
        "email": request.email,
        "password_hash": mock_data.hash_password(request.password),
        "role": request.role,
        "is_active": True,
    }

    mock_data.USERS[user_id] = user

    token = f"mock-token-{user_id}"
    mock_data.TOKENS[token] = user_id

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": public_user(user),
    }


@router.post("/login",response_model=AuthResponse,)

async def login(request: LoginRequest):
    user = mock_data.get_user_by_email(request.email)

    # Do not reveal whether the email exists.
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not mock_data.verify_password(
        request.password,
        user["password_hash"],
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    token = f"mock-token-{user['id']}"
    mock_data.TOKENS[token] = user["id"]

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": public_user(user),
    }


@router.get("/me",response_model=UserResponse,)
async def get_me(
    current_user=Depends(get_current_user),
):
    return public_user(current_user)