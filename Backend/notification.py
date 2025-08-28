from fastapi import APIRouter, Form, HTTPException
from app.services.email_service import send_email

router = APIRouter(prefix="/notify", tags=["Notification"])

@router.post("/email")
async def notify_user(
    recipient: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...)
):
    try:
        send_email(subject=subject, body=body, recipient=recipient)
        return {"message": f"Email successfully sent to {recipient}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")
