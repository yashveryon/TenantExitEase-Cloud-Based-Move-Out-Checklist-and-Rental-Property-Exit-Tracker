from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from fastapi.responses import StreamingResponse
from typing import Optional, List
from uuid import uuid4
from datetime import datetime
import pandas as pd
import io

from app.services.s3_service import upload_file_to_s3
from app.services.email_service import send_email
from app.services.db_service import (
    create_exit_request,
    get_exit_requests_by_tenant,
    update_exit_request_status
)

router = APIRouter(tags=["Exit Requests"])  # Prefix handled in main.py

# ------------------------------------------------------
# POST: Submit Exit Request
# ------------------------------------------------------
@router.post("/submit")
async def submit_exit_request(
    tenant_id: str = Form(...),
    name: str = Form(...),
    room_number: str = Form(...),
    exit_reason: str = Form(...),
    email: str = Form(...),
    moveout_checklist: Optional[List[str]] = Form(None),
    supporting_document: Optional[UploadFile] = File(None)
):
    """
    Submit an exit request with optional supporting document and checklist.
    """
    try:
        request_id = str(uuid4())
        document_url = None

        if supporting_document:
            document_url = upload_file_to_s3(supporting_document, folder="exit_docs")

        request_data = {
            "request_id": request_id,
            "tenant_id": tenant_id,
            "name": name,
            "room_number": room_number,
            "exit_reason": exit_reason,
            "moveout_checklist": moveout_checklist or [],
            "supporting_document_url": document_url,
            "email": email,
            "request_status": "Pending",
            "submitted_at": datetime.utcnow().isoformat()
        }

        create_exit_request(request_data)

        send_email(
            subject="Exit Request Submitted",
            body=f"Hi {name},\n\nYour exit request has been submitted successfully.\nRequest ID: {request_id}",
            recipient=email
        )

        return {
            "message": "Exit request submitted successfully",
            "request_id": request_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit exit request: {str(e)}")

# ------------------------------------------------------
# GET: List Exit Requests for a Tenant
# ------------------------------------------------------
@router.get("/by-tenant/{tenant_id}")
async def list_exit_requests(tenant_id: str):
    """
    Get all exit requests submitted by a specific tenant.
    """
    try:
        records = get_exit_requests_by_tenant(tenant_id)
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch exit requests: {str(e)}")

# ------------------------------------------------------
# GET: Download CSV Report for Exit Requests
# ------------------------------------------------------
@router.get("/report/{tenant_id}")
async def generate_exit_report(tenant_id: str):
    """
    Download CSV report of all exit requests for a tenant.
    """
    try:
        records = get_exit_requests_by_tenant(tenant_id)
        if not records:
            raise HTTPException(status_code=404, detail="No exit records found.")

        df = pd.DataFrame(records)
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        stream.seek(0)

        return StreamingResponse(
            iter([stream.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=exit_report_{tenant_id}.csv"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

# ------------------------------------------------------
# PATCH: Update Exit Request Status
# ------------------------------------------------------
@router.patch("/update-status")
async def update_exit_status(
    request_id: str = Body(...),
    new_status: str = Body(...)
):
    """
    Update the status of an existing exit request.
    """
    valid_statuses = {"Pending", "Approved", "Rejected"}

    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status value.")

    try:
        update_exit_request_status(request_id, new_status)
        return {"message": f"Request {request_id} updated to '{new_status}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update status: {str(e)}")
