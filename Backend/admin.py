from fastapi import APIRouter, HTTPException, Body, Query
from typing import Optional, List
import boto3

from app.config.settings import settings
from app.services.db_service import (
    get_all_exit_requests,
    get_all_damage_reports,
    update_exit_request_status,
    update_exit_request_data
)

# Initialize DynamoDB (used only if needed directly)
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

router = APIRouter(tags=["Admin Dashboard"])  # prefix handled in main.py

# -------------------------
# GET: Filtered Exit Requests
# -------------------------
@router.get("/exit-requests")
async def get_all_exit_requests_filtered(
    status: Optional[str] = Query(None),
    tenant_id: Optional[str] = Query(None),
    room_number: Optional[str] = Query(None)
):
    try:
        print("🔍 Admin fetching filtered exit requests...")
        records = get_all_exit_requests()

        if status:
            records = [r for r in records if r.get("request_status") == status]
        if tenant_id:
            records = [r for r in records if r.get("tenant_id") == tenant_id]
        if room_number:
            records = [r for r in records if r.get("room_number") == room_number]

        return records
    except Exception as e:
        print("❌ Error filtering exit requests:", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve exit requests")

# -------------------------
# GET: All Damage Reports
# -------------------------
@router.get("/damage-reports")
async def get_all_damage_reports_view():
    try:
        print("🔍 Fetching all damage reports...")
        return get_all_damage_reports()
    except Exception as e:
        print("❌ Error fetching damage reports:", e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch damage reports: {str(e)}")

# -------------------------
# PATCH: Update Exit Status
# -------------------------
@router.patch("/update-exit-status")
async def update_exit_status(
    request_id: str = Body(...),
    new_status: str = Body(...)
):
    try:
        print(f"🛠 Updating status for {request_id} → {new_status}")
        return update_exit_request_status(request_id, new_status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update status: {str(e)}")

# -------------------------
# PATCH: Add Admin Notes / Edit Fields
# -------------------------
@router.patch("/update-exit-fields")
async def update_exit_fields(
    request_id: str = Body(...),
    admin_notes: Optional[str] = Body(None),
    exit_reason: Optional[str] = Body(None),
    moveout_checklist: Optional[List[str]] = Body(None)
):
    """
    Admin updates one or more fields: checklist, notes, reason.
    """
    try:
        update_fields = {}
        if admin_notes is not None:
            update_fields["admin_notes"] = admin_notes
        if exit_reason is not None:
            update_fields["exit_reason"] = exit_reason
        if moveout_checklist is not None:
            update_fields["moveout_checklist"] = moveout_checklist

        if not update_fields:
            raise HTTPException(status_code=400, detail="No update fields provided.")

        print(f"📝 Admin updating fields for {request_id}: {list(update_fields.keys())}")
        return update_exit_request_data(request_id, update_fields)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update fields: {str(e)}")

# -------------------------
# GET: Dashboard Summary Stats
# -------------------------
@router.get("/dashboard-summary")
async def dashboard_summary():
    try:
        records = get_all_exit_requests()
        total = len(records)
        approved = sum(1 for r in records if r.get("request_status") == "Approved")
        pending = sum(1 for r in records if r.get("request_status") == "Pending")
        rejected = sum(1 for r in records if r.get("request_status") == "Rejected")
        return {
            "total_requests": total,
            "approved": approved,
            "pending": pending,
            "rejected": rejected
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch summary")

# -------------------------
# GET: Export PDF Report (Stub for future)
# -------------------------
@router.get("/export/pdf")
async def export_exit_report_pdf():
    try:
        # Placeholder for future PDF report feature
        # Example: generate_pdf_report(get_all_exit_requests())
        return {"message": "PDF export feature coming soon."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate PDF")
