"""
SparePartsIQ DynamoDB Seeder
Populates AWS DynamoDB tables with complete industrial datasets:
- SparePartsIQ-Users (4 role-based users)
- SparePartsIQ-SpareParts (50 parts)
- SparePartsIQ-Suppliers (10 suppliers)
- SparePartsIQ-InventoryTransactions (200 transactions)
- SparePartsIQ-MaintenanceSchedules (20 schedules)
- SparePartsIQ-PurchaseOrders (15 purchase orders)
- SparePartsIQ-ForecastResults (90 horizon items across 30 parts)
- SparePartsIQ-ReorderRecommendations (15 recommendations)
- SparePartsIQ-Notifications (12 notifications)
"""
import boto3
import json
import time
from datetime import datetime, timedelta
from decimal import Decimal
import bcrypt

def float_to_decimal(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: float_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [float_to_decimal(v) for v in obj]
    return obj

profile = os.getenv('AWS_PROFILE')
region = os.getenv('AWS_REGION', 'ap-south-1')
session = boto3.Session(profile_name=profile, region_name=region) if profile else boto3.Session(region_name=region)
dynamodb = session.resource('dynamodb')

DEFAULT_SEED_PASSWORD = os.getenv("SEED_USER_PASSWORD", "ChangeMe@2026")

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def seed_users():
    table = dynamodb.Table("SparePartsIQ-Users")
    pwd_hash = hash_password(DEFAULT_SEED_PASSWORD)
    users = [
        {
            "user_id": "USR-INV-01",
            "name": "Vikramaditya Rao",
            "email": "inventory@sparepartsiq.com",
            "password_hash": pwd_hash,
            "role": "Inventory Manager",
            "department": "Supply Chain & Warehouse",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "user_id": "USR-MNT-02",
            "name": "Suresh Sen",
            "email": "maintenance@sparepartsiq.com",
            "password_hash": pwd_hash,
            "role": "Maintenance Team",
            "department": "Plant Maintenance & Reliability",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "user_id": "USR-PUR-03",
            "name": "Meera Kulkarni",
            "email": "purchase@sparepartsiq.com",
            "password_hash": pwd_hash,
            "role": "Purchase Manager",
            "department": "Procurement & Sourcing",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "user_id": "USR-ADM-04",
            "name": "Plant Operations Administrator",
            "email": "admin@sparepartsiq.com",
            "password_hash": pwd_hash,
            "role": "Administrator",
            "department": "Plant Operations & IT",
            "created_at": datetime.utcnow().isoformat()
        }
    ]
    print(f"Seeding {len(users)} users into SparePartsIQ-Users...")
    with table.batch_writer() as batch:
        for u in users:
            batch.put_item(Item=float_to_decimal(u))
    print("Users seeded successfully.")

def seed_spare_parts():
    table = dynamodb.Table("SparePartsIQ-SpareParts")
    with open("data/spare_parts.json") as f:
        parts = json.load(f)
    print(f"Seeding {len(parts)} parts into SparePartsIQ-SpareParts...")
    with table.batch_writer() as batch:
        for p in parts:
            p["last_updated"] = datetime.utcnow().isoformat()
            batch.put_item(Item=float_to_decimal(p))
    print("Spare parts seeded successfully.")

def seed_suppliers():
    table = dynamodb.Table("SparePartsIQ-Suppliers")
    with open("data/suppliers.json") as f:
        suppliers = json.load(f)
    print(f"Seeding {len(suppliers)} suppliers into SparePartsIQ-Suppliers...")
    with table.batch_writer() as batch:
        for s in suppliers:
            batch.put_item(Item=float_to_decimal(s))
    print("Suppliers seeded successfully.")

def seed_inventory_transactions():
    table = dynamodb.Table("SparePartsIQ-InventoryTransactions")
    with open("data/inventory_transactions.json") as f:
        transactions = json.load(f)
    print(f"Seeding {len(transactions)} transactions into SparePartsIQ-InventoryTransactions...")
    with table.batch_writer() as batch:
        for t in transactions:
            batch.put_item(Item=float_to_decimal(t))
    print("Inventory transactions seeded successfully.")

def seed_maintenance():
    table = dynamodb.Table("SparePartsIQ-MaintenanceSchedules")
    with open("data/maintenance_schedules.json") as f:
        schedules = json.load(f)
    print(f"Seeding {len(schedules)} schedules into SparePartsIQ-MaintenanceSchedules...")
    with table.batch_writer() as batch:
        for sch in schedules:
            batch.put_item(Item=float_to_decimal(sch))
    print("Maintenance schedules seeded successfully.")

def seed_purchase_orders():
    table = dynamodb.Table("SparePartsIQ-PurchaseOrders")
    with open("data/purchase_orders.json") as f:
        orders = json.load(f)
    print(f"Seeding {len(orders)} POs into SparePartsIQ-PurchaseOrders...")
    with table.batch_writer() as batch:
        for po in orders:
            batch.put_item(Item=float_to_decimal(po))
    print("Purchase orders seeded successfully.")

def seed_forecast_results():
    table = dynamodb.Table("SparePartsIQ-ForecastResults")
    with open("data/forecast_results.json") as f:
        forecasts = json.load(f)
    print(f"Seeding forecast results into SparePartsIQ-ForecastResults...")
    count = 0
    with table.batch_writer() as batch:
        for fc in forecasts:
            for horizon in ["7_days", "30_days", "90_days"]:
                item = {
                    "part_id": fc["part_id"],
                    "forecast_horizon": horizon,
                    "part_name": fc["part_name"],
                    "category": fc["category"],
                    "horizon_metrics": fc["forecast_horizons"][horizon],
                    "historical_last_30_days": fc["historical_last_30_days"],
                    "forecast_next_30_days": fc["forecast_next_30_days"],
                    "model_champion": fc.get("model_champion", "RandomForestRegressor_v1"),
                    "model_mae": fc.get("model_mae", 0.482),
                    "model_rmse": fc.get("model_rmse", 0.645),
                    "model_r2": fc.get("model_r2", 0.892),
                    "generated_at": fc["generated_at"]
                }
                batch.put_item(Item=float_to_decimal(item))
                count += 1
    print(f"Forecast results seeded successfully ({count} horizon items).")

def seed_reorder_recommendations():
    table = dynamodb.Table("SparePartsIQ-ReorderRecommendations")
    with open("data/reorder_recommendations.json") as f:
        recommendations = json.load(f)
    print(f"Seeding {len(recommendations)} recommendations into SparePartsIQ-ReorderRecommendations...")
    with table.batch_writer() as batch:
        for rec in recommendations:
            batch.put_item(Item=float_to_decimal(rec))
    print("Reorder recommendations seeded successfully.")

def seed_notifications():
    table = dynamodb.Table("SparePartsIQ-Notifications")
    with open("data/notifications.json") as f:
        notifications = json.load(f)
    print(f"Seeding {len(notifications)} notifications into SparePartsIQ-Notifications...")
    with table.batch_writer() as batch:
        for n in notifications:
            batch.put_item(Item=float_to_decimal(n))
    print("Notifications seeded successfully.")

def verify_counts():
    tables = [
        "SparePartsIQ-Users",
        "SparePartsIQ-SpareParts",
        "SparePartsIQ-Suppliers",
        "SparePartsIQ-InventoryTransactions",
        "SparePartsIQ-MaintenanceSchedules",
        "SparePartsIQ-PurchaseOrders",
        "SparePartsIQ-ForecastResults",
        "SparePartsIQ-ReorderRecommendations",
        "SparePartsIQ-Notifications"
    ]
    print("\n--- DYNAMODB VERIFICATION ---")
    for t_name in tables:
        t = dynamodb.Table(t_name)
        res = t.scan(Select='COUNT')
        print(f"  {t_name:38}: {res['Count']} items verified in AWS")

if __name__ == "__main__":
    seed_users()
    seed_spare_parts()
    seed_suppliers()
    seed_inventory_transactions()
    seed_maintenance()
    seed_purchase_orders()
    seed_forecast_results()
    seed_reorder_recommendations()
    seed_notifications()
    verify_counts()
    print("\n=== ALL DYNAMODB TABLES SEEDED AND VERIFIED IN AWS ===")
