from fastapi import Depends, HTTPException, status
from app.dependencies.security import validate_access_token


def require_roles(allowed_roles: list[str]):
    def role_checker(payload: dict = Depends(validate_access_token)):
        if payload.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return payload

    return role_checker
