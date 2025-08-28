import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
from app.config.settings import settings

# -----------------------------
# Initialize DynamoDB Resource
# -----------------------------
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

# -----------------------------
# Table Names
# -----------------------------
EXIT_REQUEST_TABLE = "TenantExitRequests"
DAMAGE_REPORT_TABLE = "TenantDamageReports"

# -----------------------------
# Table Objects
# -----------------------------
exit_table = dynamodb.Table(EXIT_REQUEST_TABLE)
damage_table = dynamodb.Table(DAMAGE_REPORT_TABLE)

# =====================================================
#                EXIT REQUEST FUNCTIONS
# =====================================================

def create_exit_request(data: dict):
    """
    Save a new exit request in the DynamoDB table.
    Supports checklist, supporting document, and exit date.
    """
    try:
        return exit_table.put_item(Item=data)
    except Exception as e:
        raise Exception(f"Failed to save exit request: {str(e)}")


def get_exit_requests_by_tenant(tenant_id: str):
    """
    Fetch all exit requests for a given tenant_id.
    Requires GSI: TenantId-index.
    """
    try:
        response = exit_table.query(
            IndexName="TenantId-index",
            KeyConditionExpression=Key("tenant_id").eq(tenant_id)
        )
        return response.get("Items", [])
    except Exception as e:
        raise Exception(f"Error fetching tenant exit requests: {str(e)}")


def update_exit_request_status(request_id: str, new_status: str):
    """
    Update the request_status of an exit request.
    """
    try:
        response = exit_table.update_item(
            Key={"request_id": request_id},
            UpdateExpression="SET request_status = :s",
            ExpressionAttributeValues={":s": new_status},
            ReturnValues="UPDATED_NEW"
        )
        return response
    except Exception as e:
        raise Exception(f"Failed to update request status: {str(e)}")


def update_exit_request_data(request_id: str, updates: dict):
    """
    Update multiple fields (notes, checklist, etc.) of an exit request.
    """
    try:
        update_expr = []
        expr_attrs = {}

        for key, value in updates.items():
            update_expr.append(f"{key} = :{key}")
            expr_attrs[f":{key}"] = value

        update_string = "SET " + ", ".join(update_expr)

        response = exit_table.update_item(
            Key={"request_id": request_id},
            UpdateExpression=update_string,
            ExpressionAttributeValues=expr_attrs,
            ReturnValues="UPDATED_NEW"
        )
        return response
    except Exception as e:
        raise Exception(f"Failed to update exit request fields: {str(e)}")


def get_all_exit_requests():
    """
    Admin view: Get all exit requests (scan-based).
    """
    try:
        response = exit_table.scan()
        return response.get("Items", [])
    except Exception as e:
        raise Exception(f"Error fetching all exit requests: {str(e)}")

# =====================================================
#                DAMAGE REPORT FUNCTIONS
# =====================================================

def create_damage_report(data: dict):
    """
    Save a damage report in the DynamoDB table.
    Supports optional document URL.
    """
    try:
        if "estimated_cost" in data and isinstance(data["estimated_cost"], float):
            data["estimated_cost"] = Decimal(str(data["estimated_cost"]))
        return damage_table.put_item(Item=data)
    except Exception as e:
        raise Exception(f"Failed to save damage report: {str(e)}")


def get_damage_reports_by_tenant(tenant_id: str):
    """
    Fetch all damage reports for a given tenant_id.
    Requires GSI: TenantId-index.
    """
    try:
        response = damage_table.query(
            IndexName="TenantId-index",
            KeyConditionExpression=Key("tenant_id").eq(tenant_id)
        )
        return response.get("Items", [])
    except Exception as e:
        raise Exception(f"Error fetching damage reports: {str(e)}")


def get_all_damage_reports():
    """
    Admin view: Get all damage reports (scan-based).
    """
    try:
        response = damage_table.scan()
        return response.get("Items", [])
    except Exception as e:
        raise Exception(f"Error fetching all damage reports: {str(e)}")
