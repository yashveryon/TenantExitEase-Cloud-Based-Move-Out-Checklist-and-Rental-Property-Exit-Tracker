from fastapi import APIRouter, Depends, Request, HTTPException
from typing import List, Dict

router = APIRouter(tags=["Tenant"])  # Prefix already set in main.py

# -----------------------------
# 🔐 Dependency: Role Check
# -----------------------------
def require_tenant_role(request: Request):
    """
    Allow access only if the session role is 'tenant'.
    """
    role = request.session.get("role")
    if role != "tenant":
        raise HTTPException(status_code=403, detail="Access forbidden: Tenant only")
    return True

# -----------------------------
# 📄 Sample In-Memory Exit Requests
# (To be replaced with DB logic)
# -----------------------------
mock_exit_requests = [
    {
        "tenant_id": "tenant1",
        "name": "Amit Roy",
        "room_number": "C103",
        "exit_reason": "Relocation for job",
        "status": "pending",
        "submitted_at": "2025-06-20",
        "document_url": None,
    },
    {
        "tenant_id": "tenant1",
        "name": "Amit Roy",
        "room_number": "C103",
        "exit_reason": "Moving to new apartment",
        "status": "approved",
        "submitted_at": "2025-06-10",
        "document_url": "https://s3.amazonaws.com/sample/file.pdf"
    },
    {
        "tenant_id": "tenant2",
        "name": "Riya Das",
        "room_number": "D204",
        "exit_reason": "Higher studies",
        "status": "pending",
        "submitted_at": "2025-06-18",
        "document_url": None
    },
]

# -----------------------------
# 📤 GET /tenant/exit-requests/{tenant_id}
# -----------------------------
@router.get("/exit-requests/{tenant_id}", response_model=List[Dict])
def get_requests_by_tenant(tenant_id: str, allowed: bool = Depends(require_tenant_role)):
    """
    Return all exit requests submitted by a specific tenant.
    """
    return [r for r in mock_exit_requests if r["tenant_id"] == tenant_id]
