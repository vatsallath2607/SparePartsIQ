from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from backend.config import TABLE_MAINTENANCE, TABLE_PARTS
from backend.db import dynamodb, decimal_to_native, native_to_decimal
from backend.auth import get_current_user, require_roles

MACHINES = [
    {"machine_id": "MCH-CNC-001", "name": "5-Axis CNC Milling Center", "criticality": "Critical", "location": "Sector A - Precision Machining"},
    {"machine_id": "MCH-CNC-002", "name": "High-Speed Lathe Unit 2", "criticality": "High", "location": "Sector A - Turning Bay"},
    {"machine_id": "MCH-HYD-101", "name": "400-Ton Hydraulic Stamping Press", "criticality": "Critical", "location": "Sector B - Heavy Stamping"},
    {"machine_id": "MCH-TUR-201", "name": "Industrial Gas Turbine Generator", "criticality": "Critical", "location": "Sector C - Power & Utilities"},
    {"machine_id": "MCH-CNV-301", "name": "Main Automated Assembly Conveyor", "criticality": "High", "location": "Sector D - Final Assembly"},
    {"machine_id": "MCH-ROB-401", "name": "KUKA 6-Axis Welding Robot", "criticality": "High", "location": "Sector B - Robotic Welding"},
    {"machine_id": "MCH-PMP-501", "name": "High-Pressure Cooling Water Pump", "criticality": "Medium", "location": "Sector C - Fluid Circulation"},
    {"machine_id": "MCH-AIR-601", "name": "Rotary Screw Air Compressor 150HP", "criticality": "Medium", "location": "Sector C - Utility Hall"}
]

router = APIRouter(prefix="/api/maintenance", tags=["Maintenance-Based Inventory Planning"])

class MaintenanceScheduleCreate(BaseModel):
    machine_id: str
    machine_name: str
    maintenance_type: str
    scheduled_date: str  # YYYY-MM-DD
    estimated_hours: int
    assigned_technician: str
    required_parts: List[dict]  # [{"part_id": "...", "part_name": "...", "quantity_required": int}]
    priority: str = "High"  # Critical, High, Medium, Low

@router.get("/machines")
def list_machines(user: dict = Depends(get_current_user)):
    return MACHINES

@router.get("/schedules")
def list_maintenance_schedules(user: dict = Depends(get_current_user)):
    table = dynamodb.Table(TABLE_MAINTENANCE)
    res = table.scan()
    items = decimal_to_native(res.get("Items", []))
    items.sort(key=lambda x: x.get("scheduled_date", ""))
    return items

@router.post("/schedules")
def create_maintenance_schedule(
    schedule: MaintenanceScheduleCreate,
    user: dict = Depends(require_roles(["Maintenance Team", "Inventory Manager"]))
):
    table = dynamodb.Table(TABLE_MAINTENANCE)
    sched_id = f"SCH-{datetime.utcnow().strftime('%Y%m')}-{uuid.uuid4().hex[:4].upper()}"
    data = schedule.dict()
    data["schedule_id"] = sched_id
    data["status"] = "Scheduled"
    data["created_at"] = datetime.utcnow().isoformat()
    data["created_by"] = user.get("name", "Maintenance Lead")
    
    table.put_item(Item=native_to_decimal(data))
    return data

@router.get("/at-risk")
def get_at_risk_maintenance(user: dict = Depends(get_current_user)):
    """
    Identifies maintenance activities that have insufficient spare parts inventory
    in stock, flagging high-risk potential machine downtime.
    """
    maint_table = dynamodb.Table(TABLE_MAINTENANCE)
    parts_table = dynamodb.Table(TABLE_PARTS)
    
    schedules = decimal_to_native(maint_table.scan().get("Items", []))
    parts_map = {p["part_id"]: p for p in decimal_to_native(parts_table.scan().get("Items", []))}
    
    at_risk_list = []
    
    for sch in schedules:
        missing_parts = []
        is_at_risk = False
        
        for req in sch.get("required_parts", []):
            if isinstance(req, str):
                pid = req
                qty_needed = 1
            elif isinstance(req, dict):
                pid = req.get("part_id")
                qty_needed = req.get("quantity_required", 1)
            else:
                continue

            part = parts_map.get(pid)
            current_stock = part.get("current_stock", 0) if part else 0
            if current_stock < qty_needed:
                is_at_risk = True
                part_name = req.get("part_name", part.get("part_name", "Unknown")) if isinstance(req, dict) else (part.get("part_name", pid) if part else pid)
                missing_parts.append({
                    "part_id": pid,
                    "part_name": part_name,
                    "quantity_required": qty_needed,
                    "current_stock": current_stock,
                    "shortage": qty_needed - current_stock,
                    "supplier_lead_time": part.get("supplier_lead_time", 14) if part else 14
                })
                
        if is_at_risk:
            at_risk_list.append({
                "schedule_id": sch["schedule_id"],
                "machine_id": sch["machine_id"],
                "machine_name": sch["machine_name"],
                "maintenance_type": sch["maintenance_type"],
                "scheduled_date": sch["scheduled_date"],
                "priority": sch.get("priority", "High"),
                "status": sch.get("status", "Scheduled"),
                "missing_parts": missing_parts,
                "risk_summary": f"{len(missing_parts)} required components currently have insufficient stock."
            })
            
    at_risk_list.sort(key=lambda x: x["scheduled_date"])
    return at_risk_list

