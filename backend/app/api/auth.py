"""
Phase 10: Authentication API routes.
Registers /login, /register, and /me endpoints.
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.auth import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.security.auth import (
    USERS_DB,
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(payload: UserRegisterRequest):
    """Register a new user and return a JWT access token."""
    username_key = payload.username.lower()
    if username_key in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    for u in USERS_DB.values():
        if u["email"].lower() == payload.email.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    user_id = f"usr_{uuid.uuid4().hex[:8]}"
    role = "admin" if payload.role == "admin" else "user"

    user_entry = {
        "id": user_id,
        "username": payload.username,
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "full_name": payload.full_name or payload.username,
        "role": role,
    }
    USERS_DB[username_key] = user_entry

    user_resp = UserResponse(
        id=user_entry["id"],
        username=user_entry["username"],
        email=user_entry["email"],
        full_name=user_entry["full_name"],
        role=user_entry["role"],
    )

    access_token = create_access_token(
        data={"sub": user_entry["username"], "role": user_entry["role"]}
    )

    return TokenResponse(access_token=access_token, token_type="bearer", user=user_resp)


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLoginRequest):
    """Authenticate user credentials and return a JWT token."""
    identifier = payload.username_or_email.lower().strip()
    target_user = None

    # Search by username or email
    if identifier in USERS_DB:
        target_user = USERS_DB[identifier]
    else:
        for u in USERS_DB.values():
            if u["email"].lower() == identifier:
                target_user = u
                break

    if not target_user or not verify_password(payload.password, target_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
        )

    user_resp = UserResponse(
        id=target_user["id"],
        username=target_user["username"],
        email=target_user["email"],
        full_name=target_user["full_name"],
        role=target_user["role"],
    )

    access_token = create_access_token(
        data={"sub": target_user["username"], "role": target_user["role"]}
    )

    return TokenResponse(access_token=access_token, token_type="bearer", user=user_resp)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """Get profile of current authenticated user."""
    return current_user
