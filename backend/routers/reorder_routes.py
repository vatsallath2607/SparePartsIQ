from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import uuid
import random
from backend.config import TABLE_REORDERS, TABLE_POS, TABLE_PARTS, TABLE_SUPPLIERS
from backend.db import dynamodb, decimal_to_native, native_to_decimal
from backend.auth import get_current_user, require_roles

router = APIRouter(prefix="/api/reorders", tags=["Intelligent Reorder Recommendations"])

class ReorderDecision(BaseModel):
    decision_notes: Optional[str] = None

@router.get("")
def list_reorder_recommendations(
    status_filter: Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    table = dynamodb.Table(TABLE_REORDERS)
    res = table.scan()
    items = decimal_to_native(res.get("Items", []))
    
    if status_filter:
        items = [i for i in items if i.get("status") == status_filter]
        
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items

@router.post("/generate")
def generate_reorder_recommendations(user: dict = Depends(get_current_user)):
    parts_table = dynamodb.Table(TABLE_PARTS)
    rec_table = dynamodb.Table(TABLE_REORDERS)
    
    parts_res = parts_table.scan()
    parts = decimal_to_native(parts_res.get("Items", []))
    
    generated = []
    now_iso = datetime.utcnow().isoformat()
    
    for p in parts:
        curr = p.get("current_stock", 0)
        rop = p.get("reorder_point", 10)
        safety = p.get("safety_stock", p.get("min_stock", 5))
        max_s = p.get("maximum_stock", p.get("max_stock", 50))
        price = p.get("unit_price", p.get("unit_cost", 1000.0))
        lead_time = p.get("lead_time_days", p.get("supplier_lead_time", 14))
        
        if curr <= rop:
            rec_id = f"REC-GEN-{p['part_id']}-{datetime.utcnow().strftime('%m%d%H%M')}"
            rec_qty = max(max_s - curr, safety * 2)
            priority = "URGENT" if curr <= safety else "HIGH"
            
            rec_item = {
                "recommendation_id": rec_id,
                "part_id": p["part_id"],
                "part_name": p.get("part_name", p.get("name")),
                "category": p.get("category", "General"),
                "current_stock": curr,
                "safety_stock": safety,
                "reorder_point": rop,
                "recommended_quantity": rec_qty,
                "incoming_po_qty": 0,
                "supplier_id": p.get("supplier_id", "SUP-001"),
                "supplier_name": p.get("supplier_name", "SKF India"),
                "supplier_lead_time": lead_time,
                "lead_time_days": lead_time,
                "supplier_rating": 4.8,
                "unit_cost": price,
                "estimated_procurement_cost": round(rec_qty * price, 2),
                "estimated_cost": round(rec_qty * price, 2),
                "recommended_reorder_date": (datetime.utcnow() + timedelta(days=2)).date().isoformat(),
                "priority": priority,
                "status": "PENDING",
                "reason": f"Current stock ({curr}) at or below ROP ({rop}). Supplier lead time is {lead_time} days.",
                "created_at": now_iso,
                "generated_at": now_iso
            }
            rec_table.put_item(Item=native_to_decimal(rec_item))
            generated.append(rec_item)
            
    return {
        "status": "SUCCESS",
        "count": len(generated),
        "recommendations_generated": generated[:5],
        "message": f"Evaluated inventory and generated {len(generated)} reorder recommendations in DynamoDB."
    }

@router.post("/{recommendation_id}/approve")
def approve_reorder_recommendation(
    recommendation_id: str,
    decision: ReorderDecision,
    user: dict = Depends(require_roles(["Purchase Manager", "Administrator"]))
):
    rec_table = dynamodb.Table(TABLE_REORDERS)
    po_table = dynamodb.Table(TABLE_POS)
    
    res = rec_table.get_item(Key={"recommendation_id": recommendation_id})
    rec = res.get("Item")
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
        
    rec_data = decimal_to_native(rec)
    rec_data["status"] = "Approved"
    rec_data["decision_notes"] = decision.decision_notes or "Approved by Purchase Manager"
    rec_data["approved_by"] = user.get("name", "Purchase Manager")
    rec_data["updated_at"] = datetime.utcnow().isoformat()
    
    rec_table.put_item(Item=native_to_decimal(rec_data))
    
    # Automatically generate corresponding Purchase Order
    po_id = f"PO-{datetime.utcnow().strftime('%Y%m')}-{uuid.uuid4().hex[:4].upper()}"
    lead_time = rec_data.get("supplier_lead_time", 14)
    expected_delivery = (datetime.utcnow() + timedelta(days=lead_time)).strftime("%Y-%m-%d")
    
    po = {
        "po_id": po_id,
        "part_id": rec_data["part_id"],
        "part_name": rec_data["part_name"],
        "supplier_id": rec_data["supplier_id"],
        "supplier_name": rec_data["supplier_name"],
        "quantity": rec_data["recommended_quantity"],
        "unit_price": rec_data["unit_cost"],
        "total_price": rec_data["estimated_procurement_cost"],
        "total_amount": rec_data["estimated_procurement_cost"],
        "order_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "expected_delivery_date": expected_delivery,
        "status": "ORDERED",
        "created_by": user.get("name", "Purchase Manager"),
        "approved_by": user.get("name", "Purchase Manager"),
        "recommendation_id": recommendation_id,
        "notes": decision.decision_notes or "Auto-generated from ML Reorder Recommendation"
    }
    po_table.put_item(Item=native_to_decimal(po))
    
    return {
        "message": f"Recommendation '{recommendation_id}' approved and converted to Purchase Order {po_id}",
        "recommendation": rec_data,
        "purchase_order": po
    }

@router.post("/{recommendation_id}/reject")
def reject_reorder_recommendation(
    recommendation_id: str,
    decision: ReorderDecision,
    user: dict = Depends(require_roles(["Purchase Manager", "Administrator"]))
):
    rec_table = dynamodb.Table(TABLE_REORDERS)
    res = rec_table.get_item(Key={"recommendation_id": recommendation_id})
    rec = res.get("Item")
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
        
    rec_data = decimal_to_native(rec)
    rec_data["status"] = "Rejected"
    rec_data["decision_notes"] = decision.decision_notes or "Rejected by Purchase Manager"
    rec_data["rejected_by"] = user.get("name", "Purchase Manager")
    rec_data["updated_at"] = datetime.utcnow().isoformat()
    
    rec_table.put_item(Item=native_to_decimal(rec_data))
    return {"message": "Recommendation rejected", "recommendation": rec_data}
