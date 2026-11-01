"""
SparePartsIQ - Complete Industrial Demonstration Dataset Generator
Generates realistic, relational industrial spare parts data:
- 50 Spare Parts across 10 industrial categories
- 10 Industrial Equipment Suppliers
- 200 Inventory Transactions
- 20 Preventive Maintenance Schedules
- 15 Purchase Orders
- 30 ML Forecast Results (7d, 30d, 90d)
- 15 Reorder Recommendations
- 12 System Notifications & Stockout Alerts
- 4 Role-based Users
"""
import json
import random
from datetime import datetime, timedelta

random.seed(42)

NOW = datetime.utcnow()

CATEGORIES = [
    "Bearings & Bushings", "Hydraulics & Fluid Power", "Pneumatics",
    "Electrical & Automation", "Motors & Drives", "Pumps & Valves",
    "Power Transmission", "Filtration", "Sensors & Instrumentation", "Fasteners & Hardware"
]

SUPPLIERS = [
    {
        "supplier_id": "SUP-001",
        "name": "SKF India Industrial Bearings Ltd",
        "category": "Bearings & Bushings",
        "contact_person": "Rajesh Sharma",
        "email": "r.sharma@skf-partner.in",
        "phone": "+91-22-6789-0101",
        "lead_time_days": 12,
        "supplier_lead_time": 12,
        "rating": 4.8,
        "city": "Pune",
        "state": "Maharashtra",
        "location": "Pune, Maharashtra"
    },
    {
        "supplier_id": "SUP-002",
        "name": "Bosch Rexroth Fluid Power Solutions",
        "category": "Hydraulics & Fluid Power",
        "contact_person": "Ananya Deshmukh",
        "email": "ananya.d@rexroth-dist.in",
        "phone": "+91-20-4567-8902",
        "lead_time_days": 18,
        "supplier_lead_time": 18,
        "rating": 4.9,
        "city": "Ahmedabad",
        "state": "Gujarat",
        "location": "Ahmedabad, Gujarat"
    },
    {
        "supplier_id": "SUP-003",
        "name": "Festo Pneumatics Automation India",
        "category": "Pneumatics",
        "contact_person": "Karthik Iyer",
        "email": "k.iyer@festo-direct.in",
        "phone": "+91-80-2345-6703",
        "lead_time_days": 8,
        "supplier_lead_time": 8,
        "rating": 4.7,
        "city": "Bengaluru",
        "state": "Karnataka",
        "location": "Bengaluru, Karnataka"
    },
    {
        "supplier_id": "SUP-004",
        "name": "Siemens Digital Drives & Automation",
        "category": "Electrical & Automation",
        "contact_person": "Vikram Sethi",
        "email": "v.sethi@siemens-solutions.in",
        "phone": "+91-124-4123-404",
        "lead_time_days": 21,
        "supplier_lead_time": 21,
        "rating": 4.9,
        "city": "Gurugram",
        "state": "Haryana",
        "location": "Gurugram, Haryana"
    },
    {
        "supplier_id": "SUP-005",
        "name": "Parker Hannifin Motion Systems",
        "category": "Pumps & Valves",
        "contact_person": "Pooja Hegde",
        "email": "pooja.h@parker-dist.in",
        "phone": "+91-44-2890-1205",
        "lead_time_days": 15,
        "supplier_lead_time": 15,
        "rating": 4.6,
        "city": "Chennai",
        "state": "Tamil Nadu",
        "location": "Chennai, Tamil Nadu"
    },
    {
        "supplier_id": "SUP-006",
        "name": "ABB Industrial Motors & Switchgears",
        "category": "Motors & Drives",
        "contact_person": "Manoj Kulkarni",
        "email": "manoj.k@abb-partner.in",
        "phone": "+91-265-234-5606",
        "lead_time_days": 14,
        "supplier_lead_time": 14,
        "rating": 4.7,
        "city": "Vadodara",
        "state": "Gujarat",
        "location": "Vadodara, Gujarat"
    },
    {
        "supplier_id": "SUP-007",
        "name": "Timken Engineered Bearings Pvt Ltd",
        "category": "Power Transmission",
        "contact_person": "Deepak Verma",
        "email": "d.verma@timken-dist.in",
        "phone": "+91-33-2211-4407",
        "lead_time_days": 16,
        "supplier_lead_time": 16,
        "rating": 4.5,
        "city": "Jamshedpur",
        "state": "Jharkhand",
        "location": "Jamshedpur, Jharkhand"
    },
    {
        "supplier_id": "SUP-008",
        "name": "Donaldson Industrial Filtration India",
        "category": "Filtration",
        "contact_person": "Arun Nair",
        "email": "arun.n@donaldson-filtration.in",
        "phone": "+91-484-256-7808",
        "lead_time_days": 7,
        "supplier_lead_time": 7,
        "rating": 4.6,
        "city": "Kochi",
        "state": "Kerala",
        "location": "Kochi, Kerala"
    },
    {
        "supplier_id": "SUP-009",
        "name": "Schneider Electric Sensor Division",
        "category": "Sensors & Instrumentation",
        "contact_person": "Sunita Patil",
        "email": "s.patil@schneider-sensors.in",
        "phone": "+91-22-3987-6509",
        "lead_time_days": 10,
        "supplier_lead_time": 10,
        "rating": 4.8,
        "city": "Mumbai",
        "state": "Maharashtra",
        "location": "Mumbai, Maharashtra"
    },
    {
        "supplier_id": "SUP-010",
        "name": "Unbrako High Tensile Fasteners",
        "category": "Fasteners & Hardware",
        "contact_person": "Harpreet Singh",
        "email": "h.singh@unbrako-fasteners.in",
        "phone": "+91-161-267-8910",
        "lead_time_days": 5,
        "supplier_lead_time": 5,
        "rating": 4.4,
        "city": "Ludhiana",
        "state": "Punjab",
        "location": "Ludhiana, Punjab"
    }
]

PARTS_SEED = [
    # Bearings (5)
    ("PRT-BRG-1001", "High Precision Spindle Bearing 7210-B", "Bearings & Bushings", "SUP-001", "SKF India", 12500, 9, 15, 20, 50, "MCH-CNC-01", "Critical", "A1-R1"),
    ("PRT-BRG-1002", "Deep Groove Ball Bearing 6308-2RS", "Bearings & Bushings", "SUP-001", "SKF India", 1850, 42, 25, 30, 100, "MCH-MOT-102", "Medium", "A1-R2"),
    ("PRT-BRG-1003", "Spherical Roller Bearing 22215-E", "Bearings & Bushings", "SUP-007", "Timken", 8400, 6, 8, 12, 30, "MCH-PRS-201", "High", "A1-R3"),
    ("PRT-BRG-1004", "Tapered Roller Bearing 32210", "Bearings & Bushings", "SUP-007", "Timken", 3200, 28, 15, 20, 60, "MCH-GBX-301", "Medium", "A1-R4"),
    ("PRT-BRG-1005", "Linear Motion Ball Bushing LMK-25", "Bearings & Bushings", "SUP-001", "SKF India", 2100, 18, 10, 15, 40, "MCH-ROB-401", "Medium", "A1-R5"),

    # Hydraulics (5)
    ("PRT-HYD-2001", "Proportional Directional Control Valve 4WRPE", "Hydraulics & Fluid Power", "SUP-002", "Bosch Rexroth", 45000, 3, 4, 6, 15, "MCH-HYD-101", "Critical", "B2-R1"),
    ("PRT-HYD-2002", "Hydraulic Cylinder Seal Kit Heavy Duty 100mm", "Hydraulics & Fluid Power", "SUP-002", "Bosch Rexroth", 6500, 14, 10, 15, 35, "MCH-PRS-201", "High", "B2-R2"),
    ("PRT-HYD-2003", "Variable Displacement Axial Piston Pump A10V", "Hydraulics & Fluid Power", "SUP-002", "Bosch Rexroth", 95000, 2, 2, 3, 5, "MCH-HYD-101", "Critical", "B2-R3"),
    ("PRT-HYD-2004", "Hydraulic High Pressure Filter Element 10 Micron", "Hydraulics & Fluid Power", "SUP-008", "Donaldson", 4200, 25, 15, 20, 50, "MCH-HYD-101", "Medium", "B2-R4"),
    ("PRT-HYD-2005", "Hydraulic Bladder Accumulator 10 Liter 330 Bar", "Hydraulics & Fluid Power", "SUP-002", "Bosch Rexroth", 32000, 4, 3, 5, 10, "MCH-PRS-201", "High", "B2-R5"),

    # Pneumatics (5)
    ("PRT-PNM-3001", "Pneumatic Solenoid Valve 5/2 Way 24V DC", "Pneumatics", "SUP-003", "Festo", 4800, 8, 12, 16, 40, "MCH-ROB-401", "High", "C3-R1"),
    ("PRT-PNM-3002", "Pneumatic Compact Cylinder ADVU-50-25", "Pneumatics", "SUP-003", "Festo", 6200, 19, 10, 15, 30, "MCH-PKG-501", "Medium", "C3-R2"),
    ("PRT-PNM-3003", "Air Filter Regulator Lubricator FRC-1/2", "Pneumatics", "SUP-003", "Festo", 8500, 11, 8, 12, 25, "MCH-CNC-01", "Medium", "C3-R3"),
    ("PRT-PNM-3004", "Pneumatic Rotary Actuator DRVS-25", "Pneumatics", "SUP-003", "Festo", 14500, 5, 4, 6, 15, "MCH-ROB-401", "High", "C3-R4"),
    ("PRT-PNM-3005", "Pneumatic Quick Exhaust Valve SEU-1/2", "Pneumatics", "SUP-003", "Festo", 1600, 35, 15, 20, 50, "MCH-PKG-501", "Low", "C3-R5"),

    # Electrical & Automation (5)
    ("PRT-ELC-4001", "Programmable Logic Controller CPU S7-1500", "Electrical & Automation", "SUP-004", "Siemens", 125000, 2, 2, 3, 6, "MCH-CNC-01", "Critical", "D4-R1"),
    ("PRT-ELC-4002", "Power Supply Unit 24V DC 20A SITOP", "Electrical & Automation", "SUP-004", "Siemens", 18500, 7, 5, 8, 15, "MCH-PLC-601", "High", "D4-R2"),
    ("PRT-ELC-4003", "Digital Input/Output Module 16 Channels", "Electrical & Automation", "SUP-004", "Siemens", 14000, 9, 6, 10, 20, "MCH-PLC-601", "High", "D4-R3"),
    ("PRT-ELC-4004", "Heavy Duty Contactor 3-Pole 45kW 3RT", "Electrical & Automation", "SUP-004", "Siemens", 7800, 22, 12, 18, 40, "MCH-MOT-102", "Medium", "D4-R4"),
    ("PRT-ELC-4005", "Thermal Overload Relay 28-40A", "Electrical & Automation", "SUP-004", "Siemens", 3900, 16, 8, 12, 30, "MCH-MOT-102", "Medium", "D4-R5"),

    # Motors & Drives (5)
    ("PRT-MTR-5001", "AC Servo Motor 3.5 kW with Absolute Encoder", "Motors & Drives", "SUP-004", "Siemens", 82000, 2, 2, 4, 8, "MCH-CNC-01", "Critical", "E5-R1"),
    ("PRT-MTR-5002", "Variable Frequency Drive 15 kW ACS580", "Motors & Drives", "SUP-006", "ABB", 64000, 3, 3, 5, 10, "MCH-MOT-102", "Critical", "E5-R2"),
    ("PRT-MTR-5003", "Three Phase Induction Motor 7.5 kW 4-Pole", "Motors & Drives", "SUP-006", "ABB", 38000, 4, 3, 4, 8, "MCH-PMP-701", "High", "E5-R3"),
    ("PRT-MTR-5004", "DC Brushless Servo Driver 400W", "Motors & Drives", "SUP-004", "Siemens", 26000, 6, 4, 6, 12, "MCH-ROB-401", "High", "E5-R4"),
    ("PRT-MTR-5005", "Stepper Motor High Torque NEMA 34", "Motors & Drives", "SUP-006", "ABB", 9500, 15, 8, 10, 25, "MCH-PKG-501", "Medium", "E5-R5"),

    # Pumps & Valves (5)
    ("PRT-PMP-6001", "Industrial Centrifugal Coolant Pump 0.75kW", "Pumps & Valves", "SUP-005", "Parker", 21500, 5, 4, 6, 12, "MCH-CNC-01", "High", "F6-R1"),
    ("PRT-PMP-6002", "Pneumatic Diaphragm Pump 1-Inch Teflon", "Pumps & Valves", "SUP-005", "Parker", 42000, 3, 2, 4, 8, "MCH-PNT-801", "High", "F6-R2"),
    ("PRT-PMP-6003", "High Pressure Ball Valve Stainless Steel 2-Inch", "Pumps & Valves", "SUP-005", "Parker", 7800, 18, 10, 15, 35, "MCH-HYD-101", "Medium", "F6-R3"),
    ("PRT-PMP-6004", "Mechanical Shaft Seal Kit SiC/SiC/Viton", "Pumps & Valves", "SUP-005", "Parker", 4900, 12, 8, 12, 25, "MCH-PMP-701", "Medium", "F6-R4"),
    ("PRT-PMP-6005", "Non-Return Check Valve 3000 PSI", "Pumps & Valves", "SUP-005", "Parker", 3400, 24, 12, 16, 40, "MCH-HYD-101", "Low", "F6-R5"),

    # Power Transmission (5)
    ("PRT-PWR-7001", "Helical Gearbox Drive Unit Ratio 25:1", "Power Transmission", "SUP-007", "Timken", 78000, 1, 2, 3, 6, "MCH-CNV-901", "Critical", "G7-R1"),
    ("PRT-PWR-7002", "Industrial Timing Belt HTD 1440-8M-50", "Power Transmission", "SUP-007", "Timken", 3200, 38, 20, 25, 60, "MCH-CNV-901", "Low", "G7-R2"),
    ("PRT-PWR-7003", "Precision Roller Chain 80-2 Duplex 10ft", "Power Transmission", "SUP-007", "Timken", 5600, 15, 10, 15, 30, "MCH-CNV-901", "Medium", "G7-R3"),
    ("PRT-PWR-7004", "Flexible Jaw Coupling Spider Element GR-42", "Power Transmission", "SUP-007", "Timken", 1450, 45, 20, 25, 80, "MCH-MOT-102", "Low", "G7-R4"),
    ("PRT-PWR-7005", "Cone Clamping Element B-Loc 45x75", "Power Transmission", "SUP-007", "Timken", 2800, 20, 10, 15, 40, "MCH-GBX-301", "Low", "G7-R5"),

    # Filtration (5)
    ("PRT-FLT-8001", "HEPA Cleanroom Filter Panel 610x610x150", "Filtration", "SUP-008", "Donaldson", 12500, 8, 6, 10, 20, "MCH-CLN-001", "High", "H8-R1"),
    ("PRT-FLT-8002", "Air Intake Cartridge Filter 325x660mm", "Filtration", "SUP-008", "Donaldson", 4800, 26, 15, 20, 50, "MCH-CMP-002", "Medium", "H8-R2"),
    ("PRT-FLT-8003", "Oil Coalescing Filter Cartridge 0.01 Micron", "Filtration", "SUP-008", "Donaldson", 3600, 19, 12, 15, 35, "MCH-CMP-002", "Medium", "H8-R3"),
    ("PRT-FLT-8004", "Stainless Steel Wire Mesh Strainer 100 Mesh", "Filtration", "SUP-008", "Donaldson", 2200, 32, 15, 20, 60, "MCH-PMP-701", "Low", "H8-R4"),
    ("PRT-FLT-8005", "Suction Filter Element with Bypass 125 Micron", "Filtration", "SUP-008", "Donaldson", 2900, 14, 10, 14, 30, "MCH-HYD-101", "Medium", "H8-R5"),

    # Sensors & Instrumentation (5)
    ("PRT-SNS-9001", "Inductive Proximity Sensor M18 PNP NO Flush", "Sensors & Instrumentation", "SUP-009", "Schneider", 2400, 52, 25, 35, 100, "MCH-CNC-01", "Low", "I9-R1"),
    ("PRT-SNS-9002", "Optical Retroreflective Photoelectric Sensor", "Sensors & Instrumentation", "SUP-009", "Schneider", 3800, 27, 15, 20, 50, "MCH-PKG-501", "Medium", "I9-R2"),
    ("PRT-SNS-9003", "Electronic Pressure Transmitter 0-250 Bar 4-20mA", "Sensors & Instrumentation", "SUP-009", "Schneider", 8900, 6, 5, 8, 15, "MCH-HYD-101", "High", "I9-R3"),
    ("PRT-SNS-9004", "RTD PT100 Temperature Sensor Probe 150mm", "Sensors & Instrumentation", "SUP-009", "Schneider", 2100, 34, 15, 20, 60, "MCH-FUR-003", "Low", "I9-R4"),
    ("PRT-SNS-9005", "Incremental Rotary Encoder 1024 PPR 24V", "Sensors & Instrumentation", "SUP-009", "Schneider", 11200, 7, 6, 8, 16, "MCH-ROB-401", "High", "I9-R5"),

    # Fasteners & Hardware (5)
    ("PRT-FST-0001", "Hex Socket Head Cap Screws M12x50 Grade 12.9", "Fasteners & Hardware", "SUP-010", "Unbrako", 45, 480, 200, 300, 1000, "MCH-ALL-000", "Low", "J0-R1"),
    ("PRT-FST-0002", "High Tensile Stud Bolts M16x100 Grade 8.8", "Fasteners & Hardware", "SUP-010", "Unbrako", 85, 250, 150, 200, 600, "MCH-ALL-000", "Low", "J0-R2"),
    ("PRT-FST-0003", "Shim Pack Stainless Steel 0.05-1.0mm 50x50", "Fasteners & Hardware", "SUP-010", "Unbrako", 650, 40, 20, 30, 80, "MCH-PRS-201", "Low", "J0-R3"),
    ("PRT-FST-0004", "Spring Dowel Pins ISO 8752 8x40mm", "Fasteners & Hardware", "SUP-010", "Unbrako", 25, 350, 150, 250, 800, "MCH-ALL-000", "Low", "J0-R4"),
    ("PRT-FST-0005", "Copper Sealing Ring Gasket 22x27x1.5mm", "Fasteners & Hardware", "SUP-010", "Unbrako", 35, 420, 200, 300, 900, "MCH-HYD-101", "Low", "J0-R5")
]

# Generate 50 parts with dual key support (part_name & name, unit_cost & unit_price)
spare_parts = []
for p in PARTS_SEED:
    part_id, name, cat, sup_id, mfr, price, stock, safety, rop, max_stock, comp, crit, loc = p
    sup = next(s for s in SUPPLIERS if s["supplier_id"] == sup_id)
    status = "CRITICAL" if stock <= safety else ("LOW" if stock <= rop else ("OVERSTOCKED" if stock > max_stock else "HEALTHY"))
    spare_parts.append({
        "part_id": part_id,
        "part_name": name,
        "name": name,
        "category": cat,
        "description": f"Industrial grade {name} engineered for heavy manufacturing reliability.",
        "manufacturer": mfr,
        "supplier_id": sup_id,
        "supplier_name": sup["name"],
        "unit_cost": price,
        "unit_price": price,
        "current_stock": stock,
        "safety_stock": safety,
        "min_stock": safety,
        "reorder_point": rop,
        "maximum_stock": max_stock,
        "max_stock": max_stock,
        "machine_compatibility": [comp] if comp != "MCH-ALL-000" else ["MCH-CNC-01", "MCH-HYD-101", "MCH-PRS-201", "MCH-ROB-401"],
        "criticality_level": crit,
        "stock_status": status,
        "supplier_lead_time": sup["lead_time_days"],
        "lead_time_days": sup["lead_time_days"],
        "warehouse_location": loc,
        "location": loc,
        "avg_daily_consumption": round(random.uniform(0.3, 1.8), 2),
        "created_at": (NOW - timedelta(days=90)).isoformat(),
        "last_updated": NOW.isoformat()
    })

# 20 Maintenance Schedules
MACHINES = [
    ("MCH-CNC-01", "5-Axis CNC Milling Center Makino D500", "Machining Bay 1"),
    ("MCH-HYD-101", "Heavy Hydraulic Forging Station 500-Ton", "Press Shop"),
    ("MCH-PRS-201", "Mechanical Stamping Press Schuler 400T", "Stamping Bay"),
    ("MCH-ROB-401", "Articulated Robotic Welding Cell Kuka KR16", "Assembly Bay 2"),
    ("MCH-MOT-102", "Continuous Extrusion Line Drive 45kW", "Extrusion Dept"),
    ("MCH-PMP-701", "Central Chemical Coolant Supply Unit", "Utility Plant"),
    ("MCH-CNV-901", "Heavy Material Handling Roller Conveyor", "Logistics Bay"),
    ("MCH-CMP-002", "Atlas Copco Rotary Screw Compressor 75kW", "Pneumatics Room")
]

maintenance_schedules = []
for i in range(1, 21):
    m_id, m_name, location = MACHINES[(i - 1) % len(MACHINES)]
    freq = ["Weekly", "Bi-Weekly", "Monthly", "Quarterly", "Bi-Annual"][(i - 1) % 5]
    days_ahead = (i * 3) - 10
    sched_date = (NOW + timedelta(days=days_ahead)).date().isoformat()
    last_date = (NOW + timedelta(days=days_ahead - 30)).date().isoformat()
    
    cat = CATEGORIES[(i - 1) % len(CATEGORIES)]
    matching_parts = [p["part_id"] for p in spare_parts if p["category"] == cat]
    req_parts = matching_parts[:2] if matching_parts else ["PRT-BRG-1001"]

    status = "OVERDUE" if days_ahead < 0 else ("IN_PROGRESS" if days_ahead <= 2 else "SCHEDULED")
    priority = "CRITICAL" if status == "OVERDUE" else ("HIGH" if days_ahead <= 5 else "MEDIUM")

    maintenance_schedules.append({
        "schedule_id": f"SCH-2026-{i:03d}",
        "machine_id": m_id,
        "machine_name": m_name,
        "location": location,
        "frequency": freq,
        "maintenance_type": "Preventive" if i % 3 != 0 else "Condition-Based",
        "scheduled_date": sched_date,
        "last_maintenance_date": last_date,
        "status": status,
        "priority": priority,
        "required_parts": req_parts,
        "assigned_technician": ["Ramesh Pawar", "Dinesh Sharma", "Manoj Kumar", "Sunil Verma"][i % 4],
        "estimated_hours": [2, 4, 6, 8][i % 4],
        "estimated_duration_hours": [2, 4, 6, 8][i % 4],
        "created_at": (NOW - timedelta(days=60)).isoformat(),
        "created_by": "Maintenance Monitor"
    })

# 15 Purchase Orders
purchase_orders = []
po_statuses = ["PENDING", "APPROVED", "ORDERED", "RECEIVED", "CANCELLED"]
for i in range(1, 16):
    sup = SUPPLIERS[(i - 1) % len(SUPPLIERS)]
    cat_parts = [p for p in spare_parts if p["supplier_id"] == sup["supplier_id"]]
    part = cat_parts[0] if cat_parts else spare_parts[0]
    qty = random.randint(5, 30)
    status = po_statuses[(i - 1) % len(po_statuses)]
    order_date = (NOW - timedelta(days=30 - i * 2)).date().isoformat()
    delivery_date = (NOW + timedelta(days=sup["lead_time_days"] - (30 - i * 2))).date().isoformat()

    purchase_orders.append({
        "po_id": f"PO-2026-{i:03d}",
        "part_id": part["part_id"],
        "part_name": part["part_name"],
        "supplier_id": sup["supplier_id"],
        "supplier_name": sup["name"],
        "quantity": qty,
        "unit_price": part["unit_price"],
        "total_price": qty * part["unit_price"],
        "total_amount": qty * part["unit_price"],
        "status": status,
        "order_date": order_date,
        "expected_delivery_date": delivery_date,
        "received_quantity": qty if status == "RECEIVED" else 0,
        "created_by": "USR-PUR-03",
        "approved_by": "Vikramaditya Rao" if status in ["APPROVED", "ORDERED", "RECEIVED"] else None,
        "notes": f"Batch procurement for {part['part_name'][:30]} - regular replenishment.",
        "created_at": order_date + "T10:00:00Z"
    })

# 200 Inventory Transactions
transactions = []
txn_types = ["IN", "OUT", "ADJUSTMENT"]
for i in range(1, 201):
    part = spare_parts[(i - 1) % len(spare_parts)]
    ttype = random.choices(["IN", "OUT", "ADJUSTMENT"], weights=[0.35, 0.55, 0.10])[0]
    qty = random.randint(1, 15)
    days_ago = (200 - i) * 0.45
    t_time = (NOW - timedelta(days=days_ago, hours=random.randint(1, 12))).isoformat()
    
    ref = f"PO-2026-{(i % 15) + 1:03d}" if ttype == "IN" else (f"WO-MNT-{(i % 20) + 1:03d}" if ttype == "OUT" else "AUDIT-CYCLE-Q1")

    transactions.append({
        "transaction_id": f"TXN-2026-{i:05d}",
        "part_id": part["part_id"],
        "part_name": part["part_name"],
        "transaction_type": ttype,
        "quantity": qty,
        "previous_stock": part["current_stock"] + (qty if ttype == "OUT" else -qty),
        "new_stock": part["current_stock"],
        "reference_id": ref,
        "reason": f"Standard {ttype} movement for production line",
        "performed_by": random.choice(["USR-INV-01", "USR-MNT-02", "USR-PUR-03"]),
        "timestamp": t_time,
        "notes": f"Standard {ttype} movement for {part['part_name'][:30]}"
    })

# 30 Forecast Results (7d, 30d, 90d)
forecast_results = []
for i in range(30):
    part = spare_parts[i]
    avg_d = round(random.uniform(0.5, 3.5), 2)
    
    h7_demand = round(avg_d * 7, 1)
    h30_demand = round(avg_d * 30, 1)
    h90_demand = round(avg_d * 90, 1)

    hist_series = [max(0, round(random.gauss(avg_d, 0.6), 1)) for _ in range(30)]
    fc_series = [max(0, round(random.gauss(avg_d, 0.5), 1)) for _ in range(30)]

    forecast_results.append({
        "part_id": part["part_id"],
        "part_name": part["part_name"],
        "category": part["category"],
        "current_stock": part["current_stock"],
        "safety_stock": part["safety_stock"],
        "reorder_point": part["reorder_point"],
        "forecast_horizons": {
            "7_days": {
                "predicted_demand": h7_demand,
                "confidence_lower": round(h7_demand * 0.85, 1),
                "confidence_upper": round(h7_demand * 1.15, 1),
                "stockout_risk": "HIGH" if part["current_stock"] < h7_demand else "LOW"
            },
            "30_days": {
                "predicted_demand": h30_demand,
                "confidence_lower": round(h30_demand * 0.82, 1),
                "confidence_upper": round(h30_demand * 1.18, 1),
                "stockout_risk": "CRITICAL" if part["current_stock"] < h30_demand else ("HIGH" if part["current_stock"] < h30_demand * 1.2 else "LOW")
            },
            "90_days": {
                "predicted_demand": h90_demand,
                "confidence_lower": round(h90_demand * 0.78, 1),
                "confidence_upper": round(h90_demand * 1.22, 1),
                "stockout_risk": "CRITICAL" if part["current_stock"] < h90_demand * 0.7 else "MEDIUM"
            }
        },
        "historical_last_30_days": hist_series,
        "forecast_next_30_days": fc_series,
        "model_champion": "RandomForestRegressor_v1",
        "model_mae": 0.482,
        "model_rmse": 0.645,
        "model_r2": 0.892,
        "generated_at": NOW.isoformat()
    })

# 15 Reorder Recommendations
reorder_recommendations = []
low_parts = [p for p in spare_parts if p["stock_status"] in ["CRITICAL", "LOW"]]
target_parts = (low_parts + spare_parts)[:15]

for i, p in enumerate(target_parts):
    sup = next(s for s in SUPPLIERS if s["supplier_id"] == p["supplier_id"])
    avg_daily = round(random.uniform(0.6, 2.5), 2)
    rop = round(avg_daily * sup["lead_time_days"] + p["safety_stock"])
    rec_qty = max(p["maximum_stock"] - p["current_stock"], p["safety_stock"] * 2)

    priority = "URGENT" if p["current_stock"] <= p["safety_stock"] else ("HIGH" if p["current_stock"] <= rop else "MEDIUM")

    reorder_recommendations.append({
        "recommendation_id": f"REC-2026-{(i + 1):03d}",
        "part_id": p["part_id"],
        "part_name": p["part_name"],
        "category": p["category"],
        "current_stock": p["current_stock"],
        "safety_stock": p["safety_stock"],
        "reorder_point": rop,
        "recommended_quantity": rec_qty,
        "incoming_po_qty": 0 if i % 2 == 0 else random.randint(5, 15),
        "supplier_id": sup["supplier_id"],
        "supplier_name": sup["name"],
        "supplier_lead_time": sup["lead_time_days"],
        "lead_time_days": sup["lead_time_days"],
        "supplier_rating": sup["rating"],
        "unit_cost": p["unit_price"],
        "estimated_procurement_cost": rec_qty * p["unit_price"],
        "estimated_cost": rec_qty * p["unit_price"],
        "recommended_reorder_date": (NOW + timedelta(days=2)).date().isoformat(),
        "priority": priority,
        "status": "PENDING" if i < 10 else "ORDERED",
        "generated_at": NOW.isoformat(),
        "created_at": NOW.isoformat(),
        "reason": f"Current stock ({p['current_stock']}) is at or below dynamic ROP ({rop}). Supplier lead time is {sup['lead_time_days']} days."
    })

# 12 System Notifications
notifications = [
    {
        "notification_id": "NOTIF-001",
        "recipient_role": "Purchase Manager",
        "type": "STOCKOUT_ALERT",
        "priority": "CRITICAL",
        "title": "Critical Stockout Risk: Spindle Bearing 7210-B",
        "message": "Part PRT-BRG-1001 inventory (9 units) has only 12 days coverage against 12-day lead time. Scheduled overhaul requires 4 units.",
        "read": False,
        "created_at": (NOW - timedelta(hours=1)).isoformat(),
        "created_by": "Autonomous Stockout Predictor"
    },
    {
        "notification_id": "NOTIF-002",
        "recipient_role": "Purchase Manager",
        "type": "STOCKOUT_ALERT",
        "priority": "CRITICAL",
        "title": "Critical Stockout Risk: Proportional Valve 4WRPE",
        "message": "Part PRT-HYD-2001 stock (3 units) is at safety threshold. Lead time is 18 days from Bosch Rexroth.",
        "read": False,
        "created_at": (NOW - timedelta(hours=3)).isoformat(),
        "created_by": "Autonomous Stockout Predictor"
    },
    {
        "notification_id": "NOTIF-003",
        "recipient_role": "Maintenance Team",
        "type": "MAINTENANCE_WARNING",
        "priority": "HIGH",
        "title": "Upcoming 500-Ton Forging Press Servicing",
        "message": "Preventive maintenance scheduled on MCH-HYD-101 in 3 days. Ensure High Pressure Filter Element is staged.",
        "read": False,
        "created_at": (NOW - timedelta(hours=5)).isoformat(),
        "created_by": "Maintenance Monitor"
    },
    {
        "notification_id": "NOTIF-004",
        "recipient_role": "Inventory Manager",
        "type": "REORDER_TRIGGER",
        "priority": "MEDIUM",
        "title": "Automated Reorder Engine Triggered",
        "message": "15 new replenishment recommendations calculated based on ML 30-day demand forecast.",
        "read": True,
        "created_at": (NOW - timedelta(hours=8)).isoformat(),
        "created_by": "Reorder Optimizer"
    },
    {
        "notification_id": "NOTIF-005",
        "recipient_role": "Maintenance Team",
        "type": "OVERDUE_ALERT",
        "priority": "CRITICAL",
        "title": "Overdue Maintenance: Makino D500 Milling Center",
        "message": "Scheduled weekly calibration on MCH-CNC-01 is 2 days overdue. Spindle inspection required.",
        "read": False,
        "created_at": (NOW - timedelta(hours=12)).isoformat(),
        "created_by": "Maintenance Monitor"
    },
    {
        "notification_id": "NOTIF-006",
        "recipient_role": "Purchase Manager",
        "type": "PO_UPDATE",
        "priority": "LOW",
        "title": "Purchase Order PO-2026-004 Dispatched",
        "message": "Festo India confirmed dispatch of 20 Pneumatic Compact Cylinders. Expected delivery in 3 days.",
        "read": True,
        "created_at": (NOW - timedelta(days=1)).isoformat(),
        "created_by": "Procurement Portal"
    },
    {
        "notification_id": "NOTIF-007",
        "recipient_role": "Inventory Manager",
        "type": "STOCK_ADJUSTMENT",
        "priority": "LOW",
        "title": "Cycle Count Variance Logged",
        "message": "Audit adjustment recorded for Fasteners Rack. +10 units added to system stock.",
        "read": True,
        "created_at": (NOW - timedelta(days=1, hours=4)).isoformat(),
        "created_by": "Warehouse Audit"
    },
    {
        "notification_id": "NOTIF-008",
        "recipient_role": "Purchase Manager",
        "type": "STOCKOUT_ALERT",
        "priority": "HIGH",
        "title": "Helical Gearbox Drive Unit Stock Critical",
        "message": "Part PRT-PWR-7001 current stock is 1 unit against safety stock of 2 units. Lead time is 16 days.",
        "read": False,
        "created_at": (NOW - timedelta(days=2)).isoformat(),
        "created_by": "Autonomous Stockout Predictor"
    },
    {
        "notification_id": "NOTIF-009",
        "recipient_role": "Maintenance Team",
        "type": "MAINTENANCE_WARNING",
        "priority": "MEDIUM",
        "title": "Kuka KR16 Welding Cell Quarterly Overhaul",
        "message": "Quarterly overhaul scheduled in 8 days. Required Servo Motors and Encoders confirmed in stock.",
        "read": True,
        "created_at": (NOW - timedelta(days=2, hours=6)).isoformat(),
        "created_by": "Maintenance Monitor"
    },
    {
        "notification_id": "NOTIF-010",
        "recipient_role": "Inventory Manager",
        "type": "SUPPLIER_ALERT",
        "priority": "MEDIUM",
        "title": "Supplier Lead Time Change Noted",
        "message": "Siemens updated standard lead time for S7-1500 PLC modules from 18 to 21 days.",
        "read": True,
        "created_at": (NOW - timedelta(days=3)).isoformat(),
        "created_by": "Supplier Integration"
    },
    {
        "notification_id": "NOTIF-011",
        "recipient_role": "Purchase Manager",
        "type": "REORDER_TRIGGER",
        "priority": "HIGH",
        "title": "Reorder Approved: Spindle Bearing 7210-B",
        "message": "Reorder recommendation REC-2026-001 converted to PO-2026-015 for 40 units.",
        "read": True,
        "created_at": (NOW - timedelta(days=4)).isoformat(),
        "created_by": "Procurement Portal"
    },
    {
        "notification_id": "NOTIF-012",
        "recipient_role": "Maintenance Team",
        "type": "SYSTEM_HEALTH",
        "priority": "LOW",
        "title": "Daily Telemetry & Consumption Synced",
        "message": "Machine running hours and spare parts consumption logs successfully verified and updated.",
        "read": True,
        "created_at": (NOW - timedelta(days=5)).isoformat(),
        "created_by": "System Monitor"
    }
]

# Write all files to data/
with open("data/spare_parts.json", "w") as f:
    json.dump(spare_parts, f, indent=2)

with open("data/suppliers.json", "w") as f:
    json.dump(SUPPLIERS, f, indent=2)

with open("data/maintenance_schedules.json", "w") as f:
    json.dump(maintenance_schedules, f, indent=2)

with open("data/purchase_orders.json", "w") as f:
    json.dump(purchase_orders, f, indent=2)

with open("data/inventory_transactions.json", "w") as f:
    json.dump(transactions, f, indent=2)

with open("data/forecast_results.json", "w") as f:
    json.dump(forecast_results, f, indent=2)

with open("data/reorder_recommendations.json", "w") as f:
    json.dump(reorder_recommendations, f, indent=2)

with open("data/notifications.json", "w") as f:
    json.dump(notifications, f, indent=2)

print(f"Generated {len(spare_parts)} Spare Parts")
print(f"Generated {len(SUPPLIERS)} Suppliers")
print(f"Generated {len(maintenance_schedules)} Maintenance Schedules")
print(f"Generated {len(purchase_orders)} Purchase Orders")
print(f"Generated {len(transactions)} Inventory Transactions")
print(f"Generated {len(forecast_results)} Forecast Results")
print(f"Generated {len(reorder_recommendations)} Reorder Recommendations")
print(f"Generated {len(notifications)} System Notifications")
