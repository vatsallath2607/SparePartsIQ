"""
SparePartsIQ Local SQLite Seeder
Populates local SQLite database (sparepartsiq.db) with the complete industrial dataset.
"""
import os
import json
import sqlite3
import bcrypt
from datetime import datetime

DB_PATH = "data/sparepartsiq.db"

DEFAULT_SEED_PASSWORD = os.getenv("SEED_USER_PASSWORD", "ChangeMe@2026")

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def seed_sqlite():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Users
    pwd_hash = hash_password(DEFAULT_SEED_PASSWORD)
    users = [
        ("USR-INV-01", "Vikramaditya Rao", "inventory@sparepartsiq.com", pwd_hash, "Inventory Manager", "Supply Chain & Warehouse", datetime.utcnow().isoformat()),
        ("USR-MNT-02", "Suresh Sen", "maintenance@sparepartsiq.com", pwd_hash, "Maintenance Team", "Plant Maintenance & Reliability", datetime.utcnow().isoformat()),
        ("USR-PUR-03", "Meera Kulkarni", "purchase@sparepartsiq.com", pwd_hash, "Purchase Manager", "Procurement & Sourcing", datetime.utcnow().isoformat()),
        ("USR-ADM-04", "Plant Review Administrator", "admin@sparepartsiq.com", pwd_hash, "Administrator", "Plant Operations & IT", datetime.utcnow().isoformat())
    ]
    cursor.executemany("""
    INSERT OR REPLACE INTO users (user_id, name, email, password_hash, role, department, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, users)

    # 2. Spare Parts
    with open("data/spare_parts.json") as f:
        parts = json.load(f)
    for p in parts:
        cursor.execute("""
        INSERT OR REPLACE INTO spare_parts 
        (part_id, part_name, category, description, manufacturer, supplier_id, unit_cost, supplier_lead_time,
         machine_compatibility, criticality_level, warehouse_location, min_stock, max_stock, reorder_point,
         current_stock, avg_daily_consumption, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["part_id"], p.get("part_name", p.get("name")), p["category"], p["description"], p["manufacturer"],
            p["supplier_id"], p["unit_cost"], p["supplier_lead_time"], json.dumps(p["machine_compatibility"]),
            p["criticality_level"], p["warehouse_location"], p["min_stock"], p["max_stock"],
            p["reorder_point"], p["current_stock"], p.get("avg_daily_consumption", 0.5), p.get("last_updated", datetime.utcnow().isoformat())
        ))

    # 3. Suppliers
    with open("data/suppliers.json") as f:
        suppliers = json.load(f)
    for s in suppliers:
        cursor.execute("""
        INSERT OR REPLACE INTO suppliers (supplier_id, name, contact_person, email, phone, rating, lead_time_days, location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (s["supplier_id"], s["name"], s["contact_person"], s["email"], s["phone"], s["rating"], s["lead_time_days"], s["location"]))

    # 4. Inventory Transactions
    with open("data/inventory_transactions.json") as f:
        transactions = json.load(f)
    for t in transactions:
        cursor.execute("""
        INSERT OR REPLACE INTO inventory_transactions 
        (transaction_id, part_id, part_name, timestamp, transaction_type, quantity, previous_stock, new_stock, performed_by, reason, reference_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            t["transaction_id"], t["part_id"], t["part_name"], t["timestamp"], t["transaction_type"],
            t["quantity"], t.get("previous_stock", 0), t.get("new_stock", 0), t.get("performed_by", "USR-INV-01"),
            t.get("reason", "Inventory movement"), t.get("reference_id", "")
        ))

    # 5. Maintenance Schedules
    with open("data/maintenance_schedules.json") as f:
        schedules = json.load(f)
    for sch in schedules:
        cursor.execute("""
        INSERT OR REPLACE INTO maintenance_schedules 
        (schedule_id, machine_id, machine_name, maintenance_type, scheduled_date, status, estimated_hours, assigned_technician, required_parts, priority, created_at, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sch["schedule_id"], sch["machine_id"], sch["machine_name"], sch["maintenance_type"],
            sch["scheduled_date"], sch["status"], sch["estimated_hours"], sch["assigned_technician"],
            json.dumps(sch["required_parts"]), sch["priority"], sch.get("created_at", datetime.utcnow().isoformat()), sch.get("created_by", "System")
        ))

    # 6. Purchase Orders
    with open("data/purchase_orders.json") as f:
        pos = json.load(f)
    for po in pos:
        cursor.execute("""
        INSERT OR REPLACE INTO purchase_orders 
        (po_id, part_id, part_name, supplier_id, supplier_name, quantity, unit_price, total_price, order_date, expected_delivery_date, status, created_by, approved_by, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            po["po_id"], po["part_id"], po["part_name"], po["supplier_id"], po["supplier_name"],
            po["quantity"], po["unit_price"], po["total_price"], po["order_date"], po["expected_delivery_date"],
            po["status"], po["created_by"], po.get("approved_by"), po.get("notes")
        ))

    # 7. Forecast Results
    with open("data/forecast_results.json") as f:
        forecasts = json.load(f)
    for fc in forecasts:
        for horizon in ["7_days", "30_days", "90_days"]:
            cursor.execute("""
            INSERT OR REPLACE INTO forecast_results 
            (part_id, forecast_horizon, part_name, category, horizon_metrics, historical_last_30_days, forecast_next_30_days, generated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                fc["part_id"], horizon, fc["part_name"], fc["category"],
                json.dumps(fc["forecast_horizons"][horizon]),
                json.dumps(fc["historical_last_30_days"]),
                json.dumps(fc["forecast_next_30_days"]),
                fc["generated_at"]
            ))

    # 8. Reorder Recommendations
    with open("data/reorder_recommendations.json") as f:
        recs = json.load(f)
    for r in recs:
        cursor.execute("""
        INSERT OR REPLACE INTO reorder_recommendations 
        (recommendation_id, part_id, part_name, category, current_stock, incoming_po_qty, recommended_quantity,
         unit_cost, estimated_procurement_cost, recommended_reorder_date, supplier_id, supplier_name,
         supplier_lead_time, supplier_rating, reason, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["recommendation_id"], r["part_id"], r["part_name"], r["category"], r["current_stock"],
            r.get("incoming_po_qty", 0), r["recommended_quantity"], r["unit_cost"], r["estimated_procurement_cost"],
            r["recommended_reorder_date"], r["supplier_id"], r["supplier_name"], r["supplier_lead_time"],
            r["supplier_rating"], r["reason"], r["status"], r["created_at"]
        ))

    # 9. Notifications
    with open("data/notifications.json") as f:
        notifications = json.load(f)
    for n in notifications:
        cursor.execute("""
        INSERT OR REPLACE INTO notifications 
        (notification_id, recipient_role, type, priority, title, message, read, created_at, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            n["notification_id"], n["recipient_role"], n["type"], n["priority"], n["title"],
            n["message"], 1 if n["read"] else 0, n["created_at"], n.get("created_by", "System Monitor")
        ))

    conn.commit()
    conn.close()
    print("Successfully seeded all 9 SQLite tables!")

if __name__ == "__main__":
    seed_sqlite()
