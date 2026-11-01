"""
SparePartsIQ Zero-Cost Local SQLite Database
Guarantees 100% zero-cost operation with zero AWS cloud dependencies.
Provides robust local relational storage for all 9 platform tables.
"""
import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sparepartsiq.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        department TEXT,
        created_at TEXT
    );
    """)

    # 2. Spare Parts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spare_parts (
        part_id TEXT PRIMARY KEY,
        part_name TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        manufacturer TEXT,
        supplier_id TEXT,
        unit_cost REAL,
        supplier_lead_time INTEGER,
        machine_compatibility TEXT,
        criticality_level TEXT,
        warehouse_location TEXT,
        min_stock INTEGER,
        max_stock INTEGER,
        reorder_point INTEGER,
        current_stock INTEGER,
        avg_daily_consumption REAL,
        last_updated TEXT
    );
    """)

    # 3. Inventory Transactions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_transactions (
        transaction_id TEXT PRIMARY KEY,
        part_id TEXT NOT NULL,
        part_name TEXT,
        timestamp TEXT NOT NULL,
        transaction_type TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        previous_stock INTEGER,
        new_stock INTEGER,
        performed_by TEXT,
        reason TEXT,
        reference_id TEXT
    );
    """)

    # 4. Maintenance Schedules
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS maintenance_schedules (
        schedule_id TEXT PRIMARY KEY,
        machine_id TEXT NOT NULL,
        machine_name TEXT,
        maintenance_type TEXT,
        scheduled_date TEXT NOT NULL,
        status TEXT,
        estimated_hours INTEGER,
        assigned_technician TEXT,
        required_parts TEXT,
        priority TEXT,
        created_at TEXT,
        created_by TEXT
    );
    """)

    # 5. Suppliers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        contact_person TEXT,
        email TEXT,
        phone TEXT,
        rating REAL,
        lead_time_days INTEGER,
        location TEXT
    );
    """)

    # 6. Purchase Orders
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase_orders (
        po_id TEXT PRIMARY KEY,
        part_id TEXT NOT NULL,
        part_name TEXT,
        supplier_id TEXT,
        supplier_name TEXT,
        quantity INTEGER,
        unit_price REAL,
        total_price REAL,
        order_date TEXT,
        expected_delivery_date TEXT,
        status TEXT,
        created_by TEXT,
        approved_by TEXT,
        recommendation_id TEXT,
        notes TEXT,
        status_updated_at TEXT,
        status_notes TEXT
    );
    """)

    # 7. Forecast Results
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forecast_results (
        part_id TEXT,
        forecast_horizon TEXT,
        part_name TEXT,
        category TEXT,
        horizon_metrics TEXT,
        historical_last_30_days TEXT,
        forecast_next_30_days TEXT,
        generated_at TEXT,
        PRIMARY KEY (part_id, forecast_horizon)
    );
    """)

    # 8. Reorder Recommendations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reorder_recommendations (
        recommendation_id TEXT PRIMARY KEY,
        part_id TEXT NOT NULL,
        part_name TEXT,
        category TEXT,
        current_stock INTEGER,
        incoming_po_qty INTEGER,
        recommended_quantity INTEGER,
        unit_cost REAL,
        estimated_procurement_cost REAL,
        recommended_reorder_date TEXT,
        supplier_id TEXT,
        supplier_name TEXT,
        supplier_lead_time INTEGER,
        supplier_rating REAL,
        reason TEXT,
        status TEXT,
        decision_notes TEXT,
        approved_by TEXT,
        rejected_by TEXT,
        created_at TEXT,
        updated_at TEXT
    );
    """)

    # 9. Notifications
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        notification_id TEXT PRIMARY KEY,
        recipient_role TEXT,
        type TEXT,
        priority TEXT,
        title TEXT,
        message TEXT,
        read INTEGER DEFAULT 0,
        created_at TEXT,
        created_by TEXT
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Zero-cost local SQLite database initialized successfully at data/sparepartsiq.db")

