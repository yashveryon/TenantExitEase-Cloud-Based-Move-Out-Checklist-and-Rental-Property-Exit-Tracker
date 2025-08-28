from fastapi import APIRouter, Depends, Request, HTTPException
from typing import List, Dict, Any

# ❌ Removed redundant prefix
router = APIRouter(tags=["Landlord"])

# -----------------------------
# 🔐 Dependency: Role-based Access
# -----------------------------
def require_landlord_role(request: Request) -> bool:
    """
    Only allow access if the session role is 'landlord'.
    """
    role = request.session.get("role")
    if role != "landlord":
        raise HTTPException(status_code=403, detail="Access forbidden: Landlord only")
    return True

# -----------------------------
# 📄 Mock Data (Replace with DB fetch)
# -----------------------------
approved_exits = [
    {"name": "John Doe", "room_number": "A101", "exit_date": "2025-06-10"},
    {"name": "Priya Singh", "room_number": "B202", "exit_date": "2025-06-15"},
]

room_history = [
    {"room_number": "A101", "tenant_name": "John Doe", "move_in": "2024-01-01", "move_out": "2025-06-10"},
    {"room_number": "B202", "tenant_name": "Priya Singh", "move_in": "2023-11-01", "move_out": "2025-06-15"},
]

move_timeline = [
    {"date": "2025-06-10", "description": "John Doe moved out of Room A101"},
    {"date": "2025-06-15", "description": "Priya Singh moved out of Room B202"},
]

# -----------------------------
# 📤 GET /landlord/approved-exits
# -----------------------------
@router.get("/approved-exits", response_model=List[Dict[str, Any]])
def get_approved_exits(allowed: bool = Depends(require_landlord_role)):
    """
    Return a list of approved tenant exit requests.
    """
    return approved_exits

# -----------------------------
# 🏘️ GET /landlord/room-history
# -----------------------------
@router.get("/room-history", response_model=List[Dict[str, Any]])
def get_room_history(allowed: bool = Depends(require_landlord_role)):
    """
    Return historical room occupancy details.
    """
    return room_history

# -----------------------------
# 🕓 GET /landlord/move-timeline
# -----------------------------
@router.get("/move-timeline", response_model=List[Dict[str, Any]])
def get_move_timeline(allowed: bool = Depends(require_landlord_role)):
    """
    Return tenant movement timeline entries.
    """
    return move_timeline
