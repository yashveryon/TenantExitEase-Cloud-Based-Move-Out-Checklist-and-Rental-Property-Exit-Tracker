from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict

router = APIRouter(tags=["Authentication"])

# -----------------------------
# 🔐 Mock User Database
# Replace with real DB or hashed passwords in production
# -----------------------------
users_db: Dict[str, Dict[str, str]] = {
    "admin1": {"password": "adminpass", "role": "admin"},
    "tenant1": {"password": "tenantpass", "role": "tenant"},
    "landlord1": {"password": "landlordpass", "role": "landlord"},
    # ➕ Add more users as needed
}

# -----------------------------
# 📥 Pydantic Model for Login Request
# -----------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

# -----------------------------
# 🔓 Login Endpoint
# Validates user and sets session
# -----------------------------
@router.post("/login")
async def login(request: Request, creds: LoginRequest):
    username = creds.username.strip()
    password = creds.password.strip()

    user = users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Store user session info
    request.session["username"] = username
    request.session["role"] = user["role"]

    return JSONResponse(content={
        "message": "Login successful",
        "role": user["role"]
    })

# -----------------------------
# 🔒 Logout Endpoint
# Clears session
# -----------------------------
@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return JSONResponse(content={"message": "Logged out successfully"})
