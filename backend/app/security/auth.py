"""
Phase 10: Authentication and JWT Security.
Implements password hashing, JWT token issue/validation, user management, and FastAPI security dependencies.
"""

import hashlib
import hmac
import logging
import os
import time
from typing import Dict, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import get_settings
from app.models.auth import TokenData, UserResponse

logger = logging.getLogger(__name__)
security_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt."""
    salt = "publichealth_ai_salt_2026"
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    ).hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password."""
    return hmac.compare_digest(hash_password(plain_password), hashed_password)


# In-memory demo user database (pre-seeded with demo accounts)
USERS_DB: Dict[str, dict] = {
    "admin": {
        "id": "usr_admin_001",
        "username": "admin",
        "email": "admin@publichealth.ai",
        "hashed_password": hash_password("admin123"),
        "full_name": "Dr. Sarah Chen (Admin)",
        "role": "admin",
    },
    "user": {
        "id": "usr_demo_002",
        "username": "user",
        "email": "researcher@publichealth.ai",
        "hashed_password": hash_password("user123"),
        "full_name": "Public Health Researcher",
        "role": "user",
    },
}


def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    """Create a signed JWT access token."""
    settings = get_settings()
    to_encode = data.copy()
    expire = time.time() + (
        expires_delta or settings.jwt_access_token_expire_minutes * 60
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """Decode and validate a JWT access token."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        username: str = payload.get("sub")
        role: str = payload.get("role", "user")
        if username is None:
            return None
        return TokenData(username=username, role=role)
    except Exception as exc:
        logger.debug("Token decode error: %s", exc)
        return None


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> UserResponse:
    """FastAPI dependency: Requires a valid JWT bearer token."""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = decode_access_token(credentials.credentials)
    if not token_data or not token_data.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_dict = USERS_DB.get(token_data.username.lower())
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return UserResponse(
        id=user_dict["id"],
        username=user_dict["username"],
        email=user_dict["email"],
        full_name=user_dict["full_name"],
        role=user_dict["role"],
    )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> Optional[UserResponse]:
    """FastAPI dependency: Returns UserResponse if valid token provided, else None."""
    if not credentials or not credentials.credentials:
        return None
    try:
        return await get_current_user(credentials)
    except Exception:
        return None
