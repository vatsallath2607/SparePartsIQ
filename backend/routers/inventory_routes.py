from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid
import os
from backend.config import TABLE_PARTS, TABLE_TRANSACTIONS
from backend.db import dynamodb, decimal_to_native, native_to_decimal
from backend.auth import get_current_user, require_roles

router = APIRouter(prefix="/api/inventory", tags=["Inventory Management"])

class SparePartCreate(BaseModel):
    part_id: Optional[str] = None
    part_name: str
    category: str
    description: str
    manufacturer: str
    supplier_id: str
    unit_cost: float
    supplier_lead_time: int
    machine_compatibility: List[str]
    criticality_level: str  # Critical, High, Medium, Low
    warehouse_location: str
    min_stock: int
    max_stock: int
    reorder_point: int
    current_stock: int
    avg_daily_consumption: float = 0.5

class SparePartUpdate(BaseModel):
    part_name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    supplier_id: Optional[str] = None
    unit_cost: Optional[float] = None
    supplier_lead_time: Optional[int] = None
    machine_compatibility: Optional[List[str]] = None
    criticality_level: Optional[str] = None
    warehouse_location: Optional[str] = None
    min_stock: Optional[int] = None
    max_stock: Optional[int] = None
    reorder_point: Optional[int] = None
    current_stock: Optional[int] = None
    avg_daily_consumption: Optional[float] = None

class StockTransaction(BaseModel):
    transaction_type: str  # "IN" (restock), "OUT" (consumption), "ADJUSTMENT"
    quantity: int
    reason: str
    reference_id: Optional[str] = None  # e.g., Maintenance Schedule ID or PO ID

@router.get("")
def list_spare_parts(
    search: Optional[str] = None,
    category: Optional[str] = None,
    criticality: Optional[str] = None,
    stock_status: Optional[str] = None,  # "low", "normal", "overstocked"
    user: dict = Depends(get_current_user)
):
    table = dynamodb.Table(TABLE_PARTS)
    res = table.scan()
    parts = decimal_to_native(res.get("Items", []))
    
    # Filter in memory
    filtered = []
    for p in parts:
        if search:
            s = search.lower()
            if s not in p.get("part_name", "").lower() and \
               s not in p.get("part_id", "").lower() and \
               s not in p.get("manufacturer", "").lower():
                continue
        if category and p.get("category") != category:
            continue
        if criticality and p.get("criticality_level") != criticality:
            continue
        if stock_status == "low" and p.get("current_stock", 0) > p.get("reorder_point", 0):
            continue
        if stock_status == "overstocked" and p.get("current_stock", 0) <= p.get("max_stock", 9999):
            continue
            
        filtered.append(p)
        
    return filtered

@router.get("/low-stock")
def get_low_stock_parts(user: dict = Depends(get_current_user)):
    table = dynamodb.Table(TABLE_PARTS)
    res = table.scan()
    parts = decimal_to_native(res.get("Items", []))
    low_stock = [p for p in parts if p.get("current_stock", 0) <= p.get("reorder_point", 0)]
    return low_stock

@router.get("/overstocked")
def get_overstocked_parts(user: dict = Depends(get_current_user)):
    table = dynamodb.Table(TABLE_PARTS)
    res = table.scan()
    parts = decimal_to_native(res.get("Items", []))
    overstocked = [p for p in parts if p.get("current_stock", 0) > p.get("max_stock", 9999)]
    return overstocked

@router.get("/{part_id}")
def get_part_details(part_id: str, user: dict = Depends(get_current_user)):
    table = dynamodb.Table(TABLE_PARTS)
    res = table.get_item(Key={"part_id": part_id})
    item = res.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail=f"Spare part '{part_id}' not found")
    return decimal_to_native(item)

@router.post("", status_code=status.HTTP_201_CREATED)
def create_spare_part(
    part: SparePartCreate,
    user: dict = Depends(require_roles(["Inventory Manager", "Administrator"]))
):
    table = dynamodb.Table(TABLE_PARTS)
    part_id = part.part_id or f"PRT-GEN-{uuid.uuid4().hex[:6].upper()}"
    
    # Check if exists
    existing = table.get_item(Key={"part_id": part_id}).get("Item")
    if existing:
        raise HTTPException(status_code=400, detail=f"Part ID '{part_id}' already exists")
        
    data = part.dict()
    data["part_id"] = part_id
    data["name"] = data.get("part_name", part_id)
    data["unit_price"] = data.get("unit_cost", 0.0)
    data["lead_time_days"] = data.get("supplier_lead_time", 14)
    data["last_updated"] = datetime.utcnow().isoformat()
    
    table.put_item(Item=native_to_decimal(data))
    print(f"[INVENTORY-CREATE] Successfully registered part {part_id} ({data['part_name']}) in DynamoDB table {TABLE_PARTS} (mode={os.getenv('STORAGE_MODE', 'aws')})")
    return data

@router.put("/{part_id}")
def update_spare_part(
    part_id: str,
    part_update: SparePartUpdate,
    user: dict = Depends(require_roles(["Inventory Manager"]))
):
    table = dynamodb.Table(TABLE_PARTS)
    res = table.get_item(Key={"part_id": part_id})
    existing = res.get("Item")
    if not existing:
        raise HTTPException(status_code=404, detail="Spare part not found")
        
    existing_data = decimal_to_native(existing)
    update_data = {k: v for k, v in part_update.dict().items() if v is not None}
    existing_data.update(update_data)
    existing_data["last_updated"] = datetime.utcnow().isoformat()
    
    table.put_item(Item=native_to_decimal(existing_data))
    return existing_data

@router.delete("/{part_id}")
def delete_spare_part(
    part_id: str,
    user: dict = Depends(require_roles(["Inventory Manager"]))
):
    table = dynamodb.Table(TABLE_PARTS)
    table.delete_item(Key={"part_id": part_id})
    return {"message": f"Spare part '{part_id}' deleted successfully"}

@router.post("/{part_id}/transaction")
def record_inventory_transaction(
    part_id: str,
    tx: StockTransaction,
    user: dict = Depends(get_current_user)
):
    parts_table = dynamodb.Table(TABLE_PARTS)
    tx_table = dynamodb.Table(TABLE_TRANSACTIONS)
    
    res = parts_table.get_item(Key={"part_id": part_id})
    item = res.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Spare part not found")
        
    part_data = decimal_to_native(item)
    current = part_data.get("current_stock", 0)
    
    if tx.transaction_type == "IN":
        new_stock = current + tx.quantity
    elif tx.transaction_type == "OUT":
        if current < tx.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock. Available: {current}, Requested: {tx.quantity}")
        new_stock = current - tx.quantity
    elif tx.transaction_type == "ADJUSTMENT":
        new_stock = tx.quantity
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")
        
    part_data["current_stock"] = new_stock
    part_data["last_updated"] = datetime.utcnow().isoformat()
    parts_table.put_item(Item=native_to_decimal(part_data))
    
    # Record movement
    tx_id = f"TX-{uuid.uuid4().hex[:8].upper()}"
    tx_record = {
        "transaction_id": tx_id,
        "part_id": part_id,
        "part_name": part_data.get("part_name", ""),
        "timestamp": datetime.utcnow().isoformat(),
        "transaction_type": tx.transaction_type,
        "quantity": tx.quantity,
        "previous_stock": current,
        "new_stock": new_stock,
        "performed_by": user.get("name", "User"),
        "reason": tx.reason,
        "reference_id": tx.reference_id
    }
    tx_table.put_item(Item=native_to_decimal(tx_record))
    
    return {"message": "Transaction recorded", "new_stock": new_stock, "transaction": tx_record}

@router.get("/{part_id}/transactions")
def get_part_transactions(part_id: str, user: dict = Depends(get_current_user)):
    tx_table = dynamodb.Table(TABLE_TRANSACTIONS)
    # Scan or query GSI PartTransactionsIndex
    res = tx_table.scan()
    all_txs = decimal_to_native(res.get("Items", []))
    part_txs = [t for t in all_txs if t.get("part_id") == part_id]
    part_txs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return part_txs

