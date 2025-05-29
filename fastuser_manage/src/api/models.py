from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Types for standardized user status/roles
class UserRole:
    ADMIN = "admin"
    USER = "user"


# PUBLIC_INTERFACE
class UserBase(BaseModel):
    """Base user model exposing public user fields."""
    username: str
    email: EmailStr


# PUBLIC_INTERFACE
class UserCreate(UserBase):
    """Data for creating a new user."""
    password: str = Field(..., min_length=6)


# PUBLIC_INTERFACE
class UserUpdate(BaseModel):
    """Data for updating user profile."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


# PUBLIC_INTERFACE
class UserInDB(UserBase):
    """Stored user model (internal)."""
    hashed_password: str
    role: str = UserRole.USER
    id: int


# PUBLIC_INTERFACE
class UserPublic(UserBase):
    """Public details returned to clients."""
    id: int
    role: str


# PUBLIC_INTERFACE
class UserLogin(BaseModel):
    """User login request schema."""
    username: str
    password: str


# PUBLIC_INTERFACE
class Token(BaseModel):
    """Returned on successful login; for JWT."""
    access_token: str
    token_type: str


# PUBLIC_INTERFACE
class TokenData(BaseModel):
    """Token payload for internal token validation."""
    username: Optional[str] = None
    role: Optional[str] = None
    user_id: Optional[int] = None
