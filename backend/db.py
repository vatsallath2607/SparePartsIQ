"""
SparePartsIQ Data Access Layer
Supports zero-cost local SQLite storage (STORAGE_MODE="sqlite") as default,
and live Amazon DynamoDB (STORAGE_MODE="aws").
Guarantees transparent conversion between Python native types and DynamoDB Decimals.
"""
import os
import json
import sqlite3
from decimal import Decimal
from typing import Any, Dict, List, Optional
from backend.config import STORAGE_MODE, AWS_REGION, AWS_PROFILE
from backend.sqlite_db import get_connection

def decimal_to_native(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    elif isinstance(obj, dict):
        return {k: decimal_to_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_native(v) for v in obj]
    return obj

def native_to_decimal(obj: Any) -> Any:
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: native_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [native_to_decimal(v) for v in obj]
    return obj

class SQLiteTable:
    def __init__(self, table_name: str):
        name_map = {
            "SparePartsIQ-Users": "users",
            "SparePartsIQ-SpareParts": "spare_parts",
            "SparePartsIQ-InventoryTransactions": "inventory_transactions",
            "SparePartsIQ-MaintenanceSchedules": "maintenance_schedules",
            "SparePartsIQ-Suppliers": "suppliers",
            "SparePartsIQ-PurchaseOrders": "purchase_orders",
            "SparePartsIQ-ForecastResults": "forecast_results",
            "SparePartsIQ-ReorderRecommendations": "reorder_recommendations",
            "SparePartsIQ-Notifications": "notifications",
        }
        self.sql_table = name_map.get(table_name, table_name.lower().replace("-", "_"))

    def _deserialize_row(self, row: sqlite3.Row) -> dict:
        d = dict(row)
        for k in ["machine_compatibility", "required_parts", "horizon_metrics", "historical_last_30_days", "forecast_next_30_days"]:
            if k in d and isinstance(d[k], str):
                try:
                    d[k] = json.loads(d[k])
                except Exception:
                    pass
        if "read" in d and isinstance(d["read"], int):
            d["read"] = bool(d["read"])
        return d

    def scan(self) -> dict:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.sql_table}")
        rows = cursor.fetchall()
        items = [self._deserialize_row(r) for r in rows]
        conn.close()
        return {"Items": items}

    def get_item(self, Key: dict) -> dict:
        conn = get_connection()
        cursor = conn.cursor()
        where_clauses = [f"{k} = ?" for k in Key.keys()]
        values = list(Key.values())
        query = f"SELECT * FROM {self.sql_table} WHERE {' AND '.join(where_clauses)}"
        cursor.execute(query, values)
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"Item": self._deserialize_row(row)}
        return {}

    def query(self, IndexName: Optional[str] = None, KeyConditionExpression: Optional[str] = None, ExpressionAttributeValues: Optional[dict] = None) -> dict:
        conn = get_connection()
        cursor = conn.cursor()
        if KeyConditionExpression and ExpressionAttributeValues:
            col = KeyConditionExpression.split("=")[0].strip()
            val_placeholder = KeyConditionExpression.split("=")[1].strip()
            val = ExpressionAttributeValues.get(val_placeholder)
            cursor.execute(f"SELECT * FROM {self.sql_table} WHERE {col} = ?", (val,))
            rows = cursor.fetchall()
            items = [self._deserialize_row(r) for r in rows]
            conn.close()
            return {"Items": items}
        return self.scan()

    def put_item(self, Item: dict) -> dict:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({self.sql_table})")
        valid_cols = {row["name"] for row in cursor.fetchall()}

        item = Item.copy()
        filtered_item = {}
        for k, v in item.items():
            if k in valid_cols:
                if isinstance(v, Decimal):
                    filtered_item[k] = int(v) if v % 1 == 0 else float(v)
                elif isinstance(v, (dict, list)):
                    filtered_item[k] = json.dumps(v)
                elif isinstance(v, bool):
                    filtered_item[k] = 1 if v else 0
                else:
                    filtered_item[k] = v

        columns = list(filtered_item.keys())
        placeholders = ["?"] * len(columns)
        values = list(filtered_item.values())
        sql = f"INSERT OR REPLACE INTO {self.sql_table} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    def delete_item(self, Key: dict) -> dict:
        conn = get_connection()
        cursor = conn.cursor()
        where_clauses = [f"{k} = ?" for k in Key.keys()]
        values = list(Key.values())
        sql = f"DELETE FROM {self.sql_table} WHERE {' AND '.join(where_clauses)}"
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}

class DynamoDBZeroCostProxy:
    def Table(self, table_name: str):
        mode = os.getenv("STORAGE_MODE", STORAGE_MODE)
        if mode == "sqlite":
            return SQLiteTable(table_name)
        else:
            import boto3
            if os.getenv("AWS_EXECUTION_ENV") or not AWS_PROFILE:
                return boto3.resource('dynamodb', region_name=AWS_REGION).Table(table_name)
            try:
                session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
                return session.resource('dynamodb').Table(table_name)
            except Exception:
                return boto3.resource('dynamodb', region_name=AWS_REGION).Table(table_name)

class SNSZeroCostProxy:
    def publish(self, TopicArn: str, Subject: str, Message: str) -> dict:
        mode = os.getenv("STORAGE_MODE", STORAGE_MODE)
        if mode == "sqlite":
            return {"MessageId": f"local-sns-{os.urandom(4).hex()}"}
        else:
            import boto3
            if os.getenv("AWS_EXECUTION_ENV") or not AWS_PROFILE:
                return boto3.client('sns', region_name=AWS_REGION).publish(TopicArn=TopicArn, Subject=Subject, Message=Message)
            try:
                session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
                return session.client('sns').publish(TopicArn=TopicArn, Subject=Subject, Message=Message)
            except Exception:
                return boto3.client('sns', region_name=AWS_REGION).publish(TopicArn=TopicArn, Subject=Subject, Message=Message)

dynamodb = DynamoDBZeroCostProxy()

def get_dynamo_resource():
    return dynamodb

def get_sns_client():
    return SNSZeroCostProxy()
