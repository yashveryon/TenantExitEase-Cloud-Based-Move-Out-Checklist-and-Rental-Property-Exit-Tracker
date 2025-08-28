from pydantic import BaseModel, Field

# -----------------------------
# Public User Model (for responses)
# -----------------------------
class User(BaseModel):
    username: str = Field(..., example="admin123")
    role: str = Field(..., example="admin")  # admin / tenant / landlord


# -----------------------------
# Internal User Model with Password Hash (for DB/mock use)
# -----------------------------
class UserInDB(User):
    password_hash: str = Field(..., example="$2b$12$...")  # bcrypt or other hashed string


# -----------------------------
# Optional: For user registration input validation
# -----------------------------
class UserCreate(BaseModel):
    username: str = Field(..., example="new_user")
    password: str = Field(..., min_length=6, example="securepass123")
    role: str = Field(..., example="tenant")  # Validate against allowed roles if needed
