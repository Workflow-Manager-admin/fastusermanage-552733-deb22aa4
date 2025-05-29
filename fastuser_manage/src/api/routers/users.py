from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models import UserCreate, UserUpdate, UserPublic
from .. import db, security

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# PUBLIC_INTERFACE
@router.post("/", response_model=UserPublic, status_code=201)
def register_user(user: UserCreate):
    """User registration endpoint."""
    from ..security import get_password_hash
    if db.get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(user.password)
    user_create = UserCreate(username=user.username, email=user.email, password=hashed)
    user_data = db.create_user(user_create)
    return UserPublic(**user_data)


# PUBLIC_INTERFACE
@router.get("/me", response_model=UserPublic)
def get_my_profile(current_user=Depends(security.get_current_active_user)):
    """Fetch your own user profile."""
    return UserPublic(**current_user)


# PUBLIC_INTERFACE
@router.put("/me", response_model=UserPublic)
def update_my_profile(updates: UserUpdate, current_user=Depends(security.get_current_active_user)):
    """Update your own user profile."""
    updated = db.update_user_profile(current_user["username"], updates.dict(exclude_unset=True))
    return UserPublic(**updated)


# PUBLIC_INTERFACE
@router.get("/", response_model=List[UserPublic])
def list_users(admin_user=Depends(security.get_current_active_admin)):
    """List all users (admin only)."""
    users = db.get_all_users()
    return [UserPublic(**u) for u in users]


# PUBLIC_INTERFACE
@router.delete("/{username}", status_code=204)
def admin_delete_user(username: str, admin_user=Depends(security.get_current_active_admin)):
    """Delete the specified user (admin only)."""
    if not db.delete_user(username):
        raise HTTPException(status_code=404, detail="User not found")
    return

