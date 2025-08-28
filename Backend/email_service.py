import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError, ClientError
from app.config.settings import settings

# Initialize AWS SES client
ses_client = boto3.client(
    'ses',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.clean_region
)

def send_email(subject: str, body: str, recipient: str, html_body: str = None):
    """
    Send an email via AWS SES.
    
    :param subject: Email subject
    :param body: Plain text version of the message
    :param recipient: Recipient email address
    :param html_body: Optional HTML version of the email
    """
    try:
        message_body = {
            'Text': {'Data': body}
        }

        if html_body:
            message_body['Html'] = {'Data': html_body}

        response = ses_client.send_email(
            Source=settings.SES_EMAIL,
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': subject},
                'Body': message_body
            }
        )
        return response

    except (BotoCoreError, NoCredentialsError, ClientError) as e:
        print("❌ Failed to send SES email:", str(e))
        raise Exception(f"SES email failed: {str(e)}")
