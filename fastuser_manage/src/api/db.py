from typing import Dict, Optional, List
from .models import UserInDB, UserCreate, UserBase, UserRole

# In-memory storage for demo/demo/POC purposes
db_users: Dict[str, dict] = {}
auto_increment_id = 1

def _get_next_id():
    global auto_increment_id
    auto_increment_id += 1
    return auto_increment_id - 1

# PUBLIC_INTERFACE
def create_user(user: UserCreate, role: str = UserRole.USER) -> dict:
    """Add a new user to the DB. Returns user dict."""
    if user.username in db_users:
        raise Exception("Username already exists")
    user_dict = user.dict()
    user_dict["id"] = _get_next_id()
    user_dict["role"] = role
    user_dict["hashed_password"] = user_dict.pop("password")
    db_users[user.username] = user_dict
    return user_dict

# PUBLIC_INTERFACE
def get_user_by_username(username: str) -> Optional[dict]:
    """Look up user by username."""
    return db_users.get(username)

# PUBLIC_INTERFACE
def get_user_by_email(email: str) -> Optional[dict]:
    for v in db_users.values():
        if v.get("email") == email:
            return v
    return None

# PUBLIC_INTERFACE
def authenticate_user(username: str, password: str):
    from .security import verify_password
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

# PUBLIC_INTERFACE
def update_user_profile(username: str, updates: dict) -> dict:
    user = get_user_by_username(username)
    if user is None:
        raise Exception("User not found")
    for key in ["username", "email"]:
        if key in updates and updates[key] is not None:
            user[key] = updates[key]
    if "password" in updates and updates["password"]:
        from .security import get_password_hash
        user["hashed_password"] = get_password_hash(updates["password"])
    return user

# PUBLIC_INTERFACE
def get_all_users() -> List[dict]:
    return list(db_users.values())

# PUBLIC_INTERFACE
def delete_user(username: str) -> bool:
    if username in db_users:
        del db_users[username]
        return True
    return False
