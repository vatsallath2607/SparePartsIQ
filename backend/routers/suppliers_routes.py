from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
from backend.config import TABLE_SUPPLIERS
from backend.db import dynamodb, decimal_to_native, native_to_decimal
from backend.auth import get_current_user, require_roles

router = APIRouter(prefix="/api/suppliers", tags=["Supplier Intelligence"])

class SupplierCreate(BaseModel):
    name: str
    contact_person: str
    email: str
    phone: str
    rating: float = 4.5
    lead_time_days: int
    location: str

@router.get("")
def list_suppliers(user: dict = Depends(get_current_user)):
    table = dynamodb.Table(TABLE_SUPPLIERS)
    res = table.scan()
    items = decimal_to_native(res.get("Items", []))
    items.sort(key=lambda x: x.get("rating", 0), reverse=True)
    return items

@router.post("")
def create_supplier(
    supp: SupplierCreate,
    user: dict = Depends(require_roles(["Purchase Manager"]))
):
    table = dynamodb.Table(TABLE_SUPPLIERS)
    supp_id = f"SUP-{uuid.uuid4().hex[:4].upper()}"
    data = supp.dict()
    data["supplier_id"] = supp_id
    table.put_item(Item=native_to_decimal(data))
    return data

