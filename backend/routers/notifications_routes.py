from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
from backend.config import TABLE_NOTIFICATIONS, SNS_TOPIC_ARN
from backend.db import dynamodb, get_sns_client, decimal_to_native, native_to_decimal
from backend.auth import get_current_user

router = APIRouter(prefix="/api/notifications", tags=["Alerts & Notifications"])

class CreateAlertRequest(BaseModel):
    recipient_role: str  # "Inventory Manager", "Maintenance Team", "Purchase Manager", "All"
    alert_type: str      # "STOCKOUT_ALERT", "MAINTENANCE_WARNING", "REORDER_TRIGGER"
    priority: str        # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    title: str
    message: str

@router.get("")
def list_notifications(
    unread_only: bool = False,
    user: dict = Depends(get_current_user)
):
    table = dynamodb.Table(TABLE_NOTIFICATIONS)
    res = table.scan()
    items = decimal_to_native(res.get("Items", []))
    
    # Filter by user role or "All"
    user_role = user.get("role")
    items = [i for i in items if i.get("recipient_role") in [user_role, "All", None]]
    
    if unread_only:
        items = [i for i in items if not i.get("read", False)]
        
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items

@router.put("/{notification_id}/read")
def mark_notification_read(notification_id: str, user: dict = Depends(get_current_user)):
    table = dynamodb.Table(TABLE_NOTIFICATIONS)
    res = table.get_item(Key={"notification_id": notification_id})
    item = res.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    n_data = decimal_to_native(item)
    n_data["read"] = True
    table.put_item(Item=native_to_decimal(n_data))
    return {"message": "Notification marked as read", "notification_id": notification_id}

@router.post("/alert")
def send_alert_notification(
    req: CreateAlertRequest,
    user: dict = Depends(get_current_user)
):
    notif_id = f"NOTIF-{uuid.uuid4().hex[:6].upper()}"
    item = {
        "notification_id": notif_id,
        "recipient_role": req.recipient_role,
        "type": req.alert_type,
        "priority": req.priority,
        "title": req.title,
        "message": req.message,
        "read": False,
        "created_at": datetime.utcnow().isoformat(),
        "created_by": user.get("name", "System")
    }
    
    # Save to DynamoDB
    table = dynamodb.Table(TABLE_NOTIFICATIONS)
    table.put_item(Item=native_to_decimal(item))
    
    # Publish to AWS SNS Topic
    sns_published = False
    sns_message_id = None
    try:
        sns = get_sns_client()
        sns_resp = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"[{req.priority}] {req.title}",
            Message=f"SparePartsIQ Automated Alert:\nPriority: {req.priority}\nTarget Role: {req.recipient_role}\n\n{req.message}\n\nTimestamp: {item['created_at']}"
        )
        sns_published = True
        sns_message_id = sns_resp.get("MessageId")
    except Exception as e:
        print(f"SNS publish note: {e}")
        
    return {
        "notification": item,
        "sns_published": sns_published,
        "sns_message_id": sns_message_id
    }

