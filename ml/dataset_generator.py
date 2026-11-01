"""
SparePartsIQ Dataset Generator
Generates realistic industrial spare parts records, consumption history,
suppliers, maintenance schedules, and purchase orders.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

CATEGORIES = [
    "Hydraulics & Pneumatics",
    "Mechanical & Bearings",
    "Electrical & Automation",
    "Thermal & HVAC",
    "Valves & Piping"
]

CRITICALITY_LEVELS = ["Critical", "High", "Medium", "Low"]

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

SUPPLIERS = [
    {
        "supplier_id": "SUP-001",
        "name": "Apex Precision Components Ltd.",
        "contact_person": "Vikram Malhotra",
        "email": "orders@apexprecision.in",
        "phone": "+91-98201-11223",
        "rating": 4.8,
        "lead_time_days": 14,
        "location": "Pune, Maharashtra"
    },
    {
        "supplier_id": "SUP-002",
        "name": "Bharat Hydraulic & Fluid Dynamics",
        "contact_person": "Anita Deshmukh",
        "email": "sales@bharathydraulics.com",
        "phone": "+91-98212-33445",
        "rating": 4.5,
        "lead_time_days": 10,
        "location": "Ahmedabad, Gujarat"
    },
    {
        "supplier_id": "SUP-003",
        "name": "Siemens Industrial Automation Dist.",
        "contact_person": "Rohan Iyer",
        "email": "dist.supply@siemens-partner.in",
        "phone": "+91-98100-55667",
        "rating": 4.9,
        "lead_time_days": 21,
        "location": "Bengaluru, Karnataka"
    },
    {
        "supplier_id": "SUP-004",
        "name": "SKF Motion Technologies Partner",
        "contact_person": "Pooja Hegde",
        "email": "skf.orders@motiontech.co.in",
        "phone": "+91-98450-77889",
        "rating": 4.7,
        "lead_time_days": 12,
        "location": "Chennai, Tamil Nadu"
    },
    {
        "supplier_id": "SUP-005",
        "name": "Delta Industrial Sealings & Gaskets",
        "contact_person": "Sanjay Verma",
        "email": "contact@deltaseals.in",
        "phone": "+91-98711-88990",
        "rating": 4.2,
        "lead_time_days": 7,
        "location": "Gurugram, Haryana"
    }
]

SPARE_PARTS_DEFINITIONS = [
    {
        "part_id": "PRT-BRG-1001",
        "part_name": "High-Precision Angular Contact Bearing (7210-B)",
        "category": "Mechanical & Bearings",
        "description": "High-precision spindle bearing for 5-Axis CNC Milling spindles and high-speed lathes.",
        "manufacturer": "SKF",
        "supplier_id": "SUP-004",
        "unit_cost": 285.00,
        "supplier_lead_time": 12,
        "machine_compatibility": ["MCH-CNC-001", "MCH-CNC-002"],
        "criticality_level": "Critical",
        "warehouse_location": "Aisle 3, Rack B-04",
        "min_stock": 8,
        "max_stock": 40,
        "reorder_point": 15,
        "current_stock": 9,
        "avg_daily_consumption": 0.45
    },
    {
        "part_id": "PRT-HYD-2002",
        "part_name": "Hydraulic Proportional Valve (4WRPEH6)",
        "category": "Hydraulics & Pneumatics",
        "description": "Direct operated proportional servo valve for hydraulic stamping press position control.",
        "manufacturer": "Bosch Rexroth",
        "supplier_id": "SUP-002",
        "unit_cost": 740.00,
        "supplier_lead_time": 10,
        "machine_compatibility": ["MCH-HYD-101"],
        "criticality_level": "Critical",
        "warehouse_location": "Aisle 1, Rack A-12",
        "min_stock": 4,
        "max_stock": 20,
        "reorder_point": 8,
        "current_stock": 5,
        "avg_daily_consumption": 0.25
    },
    {
        "part_id": "PRT-PLC-3003",
        "part_name": "Simatic S7-1500 Digital Input Module (DI 16x24VDC)",
        "category": "Electrical & Automation",
        "description": "Fail-safe PLC digital input card for turbine control and main assembly lines.",
        "manufacturer": "Siemens",
        "supplier_id": "SUP-003",
        "unit_cost": 520.00,
        "supplier_lead_time": 21,
        "machine_compatibility": ["MCH-TUR-201", "MCH-CNV-301"],
        "criticality_level": "High",
        "warehouse_location": "Aisle 4, Clean Room C-01",
        "min_stock": 5,
        "max_stock": 25,
        "reorder_point": 10,
        "current_stock": 6,
        "avg_daily_consumption": 0.20
    },
    {
        "part_id": "PRT-SEAL-4004",
        "part_name": "High-Temp Viton Mechanical Shaft Seal 65mm",
        "category": "Valves & Piping",
        "description": "Fluoroelastomer high-temperature mechanical seal for water pumps and turbine auxiliaries.",
        "manufacturer": "EagleBurgmann",
        "supplier_id": "SUP-005",
        "unit_cost": 95.00,
        "supplier_lead_time": 7,
        "machine_compatibility": ["MCH-PMP-501", "MCH-TUR-201"],
        "criticality_level": "Medium",
        "warehouse_location": "Aisle 2, Bin D-18",
        "min_stock": 15,
        "max_stock": 70,
        "reorder_point": 25,
        "current_stock": 18,
        "avg_daily_consumption": 0.85
    },
    {
        "part_id": "PRT-SRV-5005",
        "part_name": "AC Servo Motor Encoder Cable 10m High-Flex",
        "category": "Electrical & Automation",
        "description": "Double-shielded drag chain encoder cable for robotic welders and CNC axis drives.",
        "manufacturer": "IGUS Chainflex",
        "supplier_id": "SUP-001",
        "unit_cost": 165.00,
        "supplier_lead_time": 14,
        "machine_compatibility": ["MCH-ROB-401", "MCH-CNC-001"],
        "criticality_level": "High",
        "warehouse_location": "Aisle 4, Rack E-03",
        "min_stock": 6,
        "max_stock": 30,
        "reorder_point": 12,
        "current_stock": 14,
        "avg_daily_consumption": 0.30
    },
    {
        "part_id": "PRT-FLT-6006",
        "part_name": "Coalescing Air Filter Element 0.01 Micron",
        "category": "Thermal & HVAC",
        "description": "Sub-micron oil removal filter cartridge for rotary screw air compressor.",
        "manufacturer": "Atlas Copco",
        "supplier_id": "SUP-002",
        "unit_cost": 120.00,
        "supplier_lead_time": 10,
        "machine_compatibility": ["MCH-AIR-601"],
        "criticality_level": "Medium",
        "warehouse_location": "Aisle 2, Bin C-07",
        "min_stock": 12,
        "max_stock": 60,
        "reorder_point": 20,
        "current_stock": 32,
        "avg_daily_consumption": 0.60
    },
    {
        "part_id": "PRT-BLT-7007",
        "part_name": "Heavy-Duty Timing Belt 14M Pitch 85mm Wide",
        "category": "Mechanical & Bearings",
        "description": "Carbon fiber reinforced synchronous drive belt for conveyor main transfer drives.",
        "manufacturer": "Gates",
        "supplier_id": "SUP-001",
        "unit_cost": 210.00,
        "supplier_lead_time": 14,
        "machine_compatibility": ["MCH-CNV-301"],
        "criticality_level": "Critical",
        "warehouse_location": "Aisle 3, Rack A-09",
        "min_stock": 5,
        "max_stock": 25,
        "reorder_point": 9,
        "current_stock": 7,
        "avg_daily_consumption": 0.28
    },
    {
        "part_id": "PRT-WLD-8008",
        "part_name": "Robotic Welding Torch Contact Tip 1.2mm CuCrZr (Pack of 25)",
        "category": "Electrical & Automation",
        "description": "Heavy-duty copper-chromium-zirconium contact tips for robotic arc welding torch.",
        "manufacturer": "TBI Industries",
        "supplier_id": "SUP-001",
        "unit_cost": 85.00,
        "supplier_lead_time": 14,
        "machine_compatibility": ["MCH-ROB-401"],
        "criticality_level": "Low",
        "warehouse_location": "Aisle 5, Bin B-02",
        "min_stock": 20,
        "max_stock": 100,
        "reorder_point": 35,
        "current_stock": 75,
        "avg_daily_consumption": 1.20
    },
    {
        "part_id": "PRT-VLV-9009",
        "part_name": "Pneumatic Directional Control Valve 5/2 Way 24VDC",
        "category": "Hydraulics & Pneumatics",
        "description": "High-flow solenoid valve for pneumatic actuators on assembly conveyor stations.",
        "manufacturer": "Festo",
        "supplier_id": "SUP-002",
        "unit_cost": 175.00,
        "supplier_lead_time": 10,
        "machine_compatibility": ["MCH-CNV-301", "MCH-CNC-002"],
        "criticality_level": "High",
        "warehouse_location": "Aisle 1, Rack C-05",
        "min_stock": 10,
        "max_stock": 50,
        "reorder_point": 18,
        "current_stock": 11,
        "avg_daily_consumption": 0.55
    },
    {
        "part_id": "PRT-THR-1010",
        "part_name": "Pt100 RTD Temperature Sensor with 4-20mA Transmitter",
        "category": "Thermal & HVAC",
        "description": "Vibration-proof platinum RTD for turbine bearing oil temperature monitoring.",
        "manufacturer": "Endress+Hauser",
        "supplier_id": "SUP-003",
        "unit_cost": 310.00,
        "supplier_lead_time": 21,
        "machine_compatibility": ["MCH-TUR-201", "MCH-PMP-501"],
        "criticality_level": "Critical",
        "warehouse_location": "Aisle 4, Bin A-14",
        "min_stock": 4,
        "max_stock": 18,
        "reorder_point": 7,
        "current_stock": 5,
        "avg_daily_consumption": 0.18
    }
]

def generate_historical_consumption(days=365):
    """
    Generate daily consumption history over past 365 days.
    Includes seasonality, maintenance spikes, weekend lower usage,
    and intermittent demand patterns characteristic of spare parts.
    """
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    
    records = []
    
    for part in SPARE_PARTS_DEFINITIONS:
        base_rate = part["avg_daily_consumption"]
        part_id = part["part_id"]
        
        current_date = start_date
        day_idx = 0
        while current_date < end_date:
            weekday = current_date.weekday() # 0-6 (Mon-Sun)
            
            # Weekend factor (lower industrial operations on Sundays)
            day_factor = 0.4 if weekday == 6 else (0.8 if weekday == 5 else 1.1)
            
            # Monthly seasonality: slight mid-quarter overhaul increase
            month_factor = 1.0 + 0.25 * np.sin(2 * np.pi * current_date.month / 12)
            
            # Intermittent demand Poisson arrival
            lambda_param = base_rate * day_factor * month_factor
            
            # Scheduled maintenance spike periodically (every ~45-60 days)
            is_maintenance_day = (day_idx % 52 == 0) and (day_idx > 0)
            if is_maintenance_day:
                consumed_qty = int(np.random.poisson(lambda_param) + np.random.randint(2, 6))
            else:
                consumed_qty = int(np.random.poisson(lambda_param))
                
            machine_utilization_pct = round(random.uniform(70.0, 96.0) if weekday < 5 else random.uniform(40.0, 65.0), 1)
            
            records.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "part_id": part_id,
                "part_name": part["part_name"],
                "category": part["category"],
                "consumed_quantity": consumed_qty,
                "machine_utilization_pct": machine_utilization_pct,
                "is_maintenance_day": 1 if is_maintenance_day else 0,
                "day_of_week": weekday,
                "month": current_date.month,
                "unit_cost": part["unit_cost"]
            })
            
            current_date += timedelta(days=1)
            day_idx += 1
            
    df = pd.DataFrame(records)
    return df

def generate_maintenance_schedules():
    """
    Generate upcoming maintenance schedules for next 90 days
    and recent completed maintenance for audit trail.
    """
    today = datetime.utcnow().date()
    schedules = [
        {
            "schedule_id": "SCH-2026-1101",
            "machine_id": "MCH-CNC-001",
            "machine_name": "5-Axis CNC Milling Center",
            "maintenance_type": "Preventive Spindle Overhaul",
            "scheduled_date": (today + timedelta(days=5)).strftime("%Y-%m-%d"),
            "status": "Scheduled",
            "estimated_hours": 8,
            "assigned_technician": "Rajesh Kumar (Lead Tech)",
            "required_parts": [
                {"part_id": "PRT-BRG-1001", "part_name": "High-Precision Angular Contact Bearing (7210-B)", "quantity_required": 4},
                {"part_id": "PRT-SRV-5005", "part_name": "AC Servo Motor Encoder Cable 10m High-Flex", "quantity_required": 2}
            ],
            "priority": "High"
        },
        {
            "schedule_id": "SCH-2026-1108",
            "machine_id": "MCH-HYD-101",
            "machine_name": "400-Ton Hydraulic Stamping Press",
            "maintenance_type": "Hydraulic System Servicing & Valve Calibration",
            "scheduled_date": (today + timedelta(days=11)).strftime("%Y-%m-%d"),
            "status": "Scheduled",
            "estimated_hours": 12,
            "assigned_technician": "Sunil Shinde",
            "required_parts": [
                {"part_id": "PRT-HYD-2002", "part_name": "Hydraulic Proportional Valve (4WRPEH6)", "quantity_required": 3}
            ],
            "priority": "Critical"
        },
        {
            "schedule_id": "SCH-2026-1115",
            "machine_id": "MCH-TUR-201",
            "machine_name": "Industrial Gas Turbine Generator",
            "maintenance_type": "Quarterly Sensor & Oil Seal Replacement",
            "scheduled_date": (today + timedelta(days=18)).strftime("%Y-%m-%d"),
            "status": "Scheduled",
            "estimated_hours": 16,
            "assigned_technician": "Amitabh Bose",
            "required_parts": [
                {"part_id": "PRT-PLC-3003", "part_name": "Simatic S7-1500 Digital Input Module", "quantity_required": 2},
                {"part_id": "PRT-SEAL-4004", "part_name": "High-Temp Viton Mechanical Shaft Seal 65mm", "quantity_required": 6},
                {"part_id": "PRT-THR-1010", "part_name": "Pt100 RTD Temperature Sensor", "quantity_required": 3}
            ],
            "priority": "Critical"
        },
        {
            "schedule_id": "SCH-2026-1122",
            "machine_id": "MCH-CNV-301",
            "machine_name": "Main Automated Assembly Conveyor",
            "maintenance_type": "Conveyor Drive Belt Replacement & Valve Check",
            "scheduled_date": (today + timedelta(days=26)).strftime("%Y-%m-%d"),
            "status": "Scheduled",
            "estimated_hours": 6,
            "assigned_technician": "Dinesh Patekar",
            "required_parts": [
                {"part_id": "PRT-BLT-7007", "part_name": "Heavy-Duty Timing Belt 14M Pitch 85mm Wide", "quantity_required": 3},
                {"part_id": "PRT-VLV-9009", "part_name": "Pneumatic Directional Control Valve 5/2 Way 24VDC", "quantity_required": 4}
            ],
            "priority": "High"
        },
        {
            "schedule_id": "SCH-2026-1205",
            "machine_id": "MCH-ROB-401",
            "machine_name": "KUKA 6-Axis Welding Robot",
            "maintenance_type": "Monthly Arc Torch Tune-Up & Tip Swap",
            "scheduled_date": (today + timedelta(days=38)).strftime("%Y-%m-%d"),
            "status": "Scheduled",
            "estimated_hours": 4,
            "assigned_technician": "Rajesh Kumar (Lead Tech)",
            "required_parts": [
                {"part_id": "PRT-WLD-8008", "part_name": "Robotic Welding Torch Contact Tip (Pack of 25)", "quantity_required": 5}
            ],
            "priority": "Medium"
        }
    ]
    return schedules

def generate_purchase_orders():
    """
    Generate recent and open purchase orders.
    """
    today = datetime.utcnow().date()
    orders = [
        {
            "po_id": "PO-2026-0901",
            "part_id": "PRT-BRG-1001",
            "part_name": "High-Precision Angular Contact Bearing (7210-B)",
            "supplier_id": "SUP-004",
            "supplier_name": "SKF Motion Technologies Partner",
            "quantity": 15,
            "unit_price": 285.00,
            "total_price": 4275.00,
            "order_date": (today - timedelta(days=8)).strftime("%Y-%m-%d"),
            "expected_delivery_date": (today + timedelta(days=4)).strftime("%Y-%m-%d"),
            "status": "In-Transit",
            "created_by": "Purchase Manager",
            "approved_by": "Purchase Manager",
            "notes": "Urgent procurement for scheduled CNC overhaul"
        },
        {
            "po_id": "PO-2026-0902",
            "part_id": "PRT-FLT-6006",
            "part_name": "Coalescing Air Filter Element 0.01 Micron",
            "supplier_id": "SUP-002",
            "supplier_name": "Bharat Hydraulic & Fluid Dynamics",
            "quantity": 20,
            "unit_price": 120.00,
            "total_price": 2400.00,
            "order_date": (today - timedelta(days=20)).strftime("%Y-%m-%d"),
            "expected_delivery_date": (today - timedelta(days=10)).strftime("%Y-%m-%d"),
            "status": "Completed",
            "created_by": "Purchase Manager",
            "approved_by": "Purchase Manager",
            "notes": "Stock replenishment"
        }
    ]
    return orders

def save_all_datasets():
    df_consumption = generate_historical_consumption(days=365)
    df_consumption.to_csv("data/historical_consumption.csv", index=False)
    print(f"Generated historical consumption: {len(df_consumption)} rows saved to data/historical_consumption.csv")
    
    with open("data/spare_parts.json", "w") as f:
        json.dump(SPARE_PARTS_DEFINITIONS, f, indent=2)
    print(f"Saved {len(SPARE_PARTS_DEFINITIONS)} spare parts to data/spare_parts.json")
    
    with open("data/suppliers.json", "w") as f:
        json.dump(SUPPLIERS, f, indent=2)
    print(f"Saved {len(SUPPLIERS)} suppliers to data/suppliers.json")
    
    schedules = generate_maintenance_schedules()
    with open("data/maintenance_schedules.json", "w") as f:
        json.dump(schedules, f, indent=2)
    print(f"Saved {len(schedules)} maintenance schedules to data/maintenance_schedules.json")
    
    orders = generate_purchase_orders()
    with open("data/purchase_orders.json", "w") as f:
        json.dump(orders, f, indent=2)
    print(f"Saved {len(orders)} purchase orders to data/purchase_orders.json")

if __name__ == "__main__":
    save_all_datasets()

