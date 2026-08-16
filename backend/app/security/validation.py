"""Input validation helpers."""

from fastapi import HTTPException


def validate_query(query: str) -> str:
    cleaned = query.strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    if len(cleaned) > 2000:
        raise HTTPException(status_code=400, detail="Query exceeds maximum length (2000)")
    return cleaned
