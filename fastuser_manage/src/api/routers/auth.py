from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..models import Token, UserLogin
from .. import db, security

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# PUBLIC_INTERFACE
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user (login) and return a JWT token."""
    user = db.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = security.create_access_token(
        data={"sub": user["username"], "user_id": user["id"], "role": user["role"]},
        expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# PUBLIC_INTERFACE
@router.post("/logout", status_code=204)
def logout():
    """Logout endpoint - noop for JWT. (frontend should discard token)"""
    # Could implement JWT blacklist in production
    return
