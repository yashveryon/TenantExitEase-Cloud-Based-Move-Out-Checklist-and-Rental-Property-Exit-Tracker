from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# -----------------------------
# 🔁 Import Routers
# -----------------------------
from app.routers import (
    exit,
    upload,
    damage,
    notification,
    admin,
    auth,
    tenant,
    landlord
)

# -----------------------------
# 🚀 Initialize FastAPI App
# -----------------------------
app = FastAPI(
    title="TenantExitEase API",
    description="API for managing tenant exit requests, uploads, damage reports, notifications, and role-based dashboards.",
    version="1.0.0"
)

# -----------------------------
# 🔐 Session Middleware
# Enables session-based auth (for role, username, etc.)
# -----------------------------
app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key"  # ⚠️ Use an environment variable in production
)

# -----------------------------
# 🌐 CORS Middleware
# Allows frontend at localhost to communicate
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# 📦 Register API Routers
# -----------------------------
app.include_router(exit.router, prefix="/exit-request")
app.include_router(upload.router, prefix="/upload")
app.include_router(damage.router, prefix="/damage-report")
app.include_router(notification.router, prefix="/notifications")
app.include_router(admin.router, prefix="/admin")
app.include_router(auth.router)  # /login, /logout
app.include_router(tenant.router, prefix="/tenant")
app.include_router(landlord.router, prefix="/landlord")

# -----------------------------
# ✅ Root Health Check
# -----------------------------
@app.get("/")
async def root():
    return {"message": "TenantExitEase backend is running ✅"}
