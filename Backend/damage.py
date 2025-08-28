# app/routers/damage.py

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi import Request
from typing import Optional, List
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

from app.services.db_service import create_damage_report, get_damage_reports_by_tenant
from app.services.s3_service import upload_file_to_s3
from app.services.email_service import send_email

router = APIRouter(tags=["Damage Reports"])  # Prefix handled in main.py

# -----------------------------
# Pydantic model for damaged items
# -----------------------------
class DamageItem(BaseModel):
    item: str
    price: float

class DamageReport(BaseModel):
    tenant_id: str
    room_number: str
    damaged_items: List[DamageItem]
    total_estimated: float

# -----------------------------
# POST: Submit JSON-Based Damage Report (modern format)
# -----------------------------
@router.post("/submit")
async def submit_damage_json(
    request: Request,
    document: Optional[UploadFile] = File(None),
    notify_email: Optional[str] = None
):
    """
    Submit a new damage report with a list of damaged items and optional document/email.
    """
    try:
        body = await request.json()
        report_id = str(uuid4())
        document_url = None

        # Upload document to S3 if present
        if document:
            document_url = upload_file_to_s3(document, folder="damage_docs")

        damage_data = {
            "report_id": report_id,
            "tenant_id": body["tenant_id"],
            "room_number": body["room_number"],
            "damaged_items": body["damaged_items"],
            "estimated_cost": body["total_estimated"],
            "document_url": document_url,
            "reported_at": datetime.utcnow().isoformat()
        }

        # Save to DB
        create_damage_report(damage_data)

        # Optional: Email notification
        if notify_email:
            send_email(
                subject="Damage Report Submitted",
                body=(
                    f"Dear Tenant,\n\nYour damage report has been submitted.\n\n"
                    f"Report ID: {report_id}\nEstimated Amount: ₹{body['total_estimated']}\n\nThank you."
                ),
                recipient=notify_email
            )

        return {
            "message": "Damage report submitted successfully",
            "report_id": report_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting damage report: {str(e)}")


# -----------------------------
# GET: List Damage Reports by Tenant ID
# -----------------------------
@router.get("/list/{tenant_id}")
async def list_damage_reports(tenant_id: str):
    """
    Get all damage reports submitted by a specific tenant.
    """
    try:
        records = get_damage_reports_by_tenant(tenant_id)
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch damage reports: {str(e)}")
