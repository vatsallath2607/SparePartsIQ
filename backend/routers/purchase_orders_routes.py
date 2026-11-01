from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import uuid
from backend.config import TABLE_POS, TABLE_PARTS
from backend.db import dynamodb, decimal_to_native, native_to_decimal
from backend.auth import get_current_user, require_roles

router = APIRouter(prefix="/api/purchase-orders", tags=["Purchase Orders & Procurement"])

class PurchaseOrderCreate(BaseModel):
    part_id: str
    part_name: str
    supplier_id: str
    supplier_name: str
    quantity: int
    unit_price: float
    notes: Optional[str] = None

class PurchaseOrderStatusUpdate(BaseModel):
    status: str  # "Ordered", "In-Transit", "Received", "Cancelled"
    notes: Optional[str] = None

@router.get("")
def list_purchase_orders(
    status_filter: Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    table = dynamodb.Table(TABLE_POS)
    res = table.scan()
    items = decimal_to_native(res.get("Items", []))
    if status_filter:
        items = [i for i in items if i.get("status") == status_filter]
    items.sort(key=lambda x: x.get("order_date", ""), reverse=True)
    return items

@router.post("")
def create_purchase_order(
    po: PurchaseOrderCreate,
    user: dict = Depends(require_roles(["Purchase Manager"]))
):
    table = dynamodb.Table(TABLE_POS)
    po_id = f"PO-{datetime.utcnow().strftime('%Y%m')}-{uuid.uuid4().hex[:4].upper()}"
    total_price = round(po.quantity * po.unit_price, 2)
    expected_delivery = (datetime.utcnow() + timedelta(days=14)).strftime("%Y-%m-%d")
    
    data = po.dict()
    data.update({
        "po_id": po_id,
        "total_price": total_price,
        "order_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "expected_delivery_date": expected_delivery,
        "status": "Ordered",
        "created_by": user.get("name", "Purchase Manager"),
        "approved_by": user.get("name", "Purchase Manager")
    })
    table.put_item(Item=native_to_decimal(data))
    return data

@router.put("/{po_id}/status")
def update_po_status(
    po_id: str,
    update: PurchaseOrderStatusUpdate,
    user: dict = Depends(require_roles(["Purchase Manager", "Inventory Manager"]))
):
    po_table = dynamodb.Table(TABLE_POS)
    res = po_table.get_item(Key={"po_id": po_id})
    po = res.get("Item")
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
        
    po_data = decimal_to_native(po)
    old_status = po_data.get("status")
    new_status = update.status
    po_data["status"] = new_status
    po_data["status_updated_at"] = datetime.utcnow().isoformat()
    if update.notes:
        po_data["status_notes"] = update.notes
        
    po_table.put_item(Item=native_to_decimal(po_data))
    
    # If received, automatically update inventory stock
    if new_status == "Received" and old_status != "Received":
        parts_table = dynamodb.Table(TABLE_PARTS)
        part_res = parts_table.get_item(Key={"part_id": po_data["part_id"]})
        part_item = part_res.get("Item")
        if part_item:
            p_data = decimal_to_native(part_item)
            p_data["current_stock"] = p_data.get("current_stock", 0) + po_data["quantity"]
            p_data["last_updated"] = datetime.utcnow().isoformat()
            parts_table.put_item(Item=native_to_decimal(p_data))
            
    return {"message": f"PO status updated to {new_status}", "purchase_order": po_data}

