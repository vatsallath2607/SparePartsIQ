import boto3
import time
import os

session = boto3.Session(profile_name='antigravity-project', region_name='ap-south-1')
dynamodb = session.client('dynamodb')

TABLES = [
    {
        "TableName": "SparePartsIQ-Users",
        "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "email", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "EmailIndex",
                "KeySchema": [{"AttributeName": "email", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"}
            }
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "SparePartsIQ-SpareParts",
        "KeySchema": [{"AttributeName": "part_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [
            {"AttributeName": "part_id", "AttributeType": "S"},
            {"AttributeName": "category", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "CategoryIndex",
                "KeySchema": [{"AttributeName": "category", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"}
            }
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "SparePartsIQ-InventoryTransactions",
        "KeySchema": [{"AttributeName": "transaction_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [
            {"AttributeName": "transaction_id", "AttributeType": "S"},
            {"AttributeName": "part_id", "AttributeType": "S"},
            {"AttributeName": "timestamp", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "PartTransactionsIndex",
                "KeySchema": [
                    {"AttributeName": "part_id", "KeyType": "HASH"},
                    {"AttributeName": "timestamp", "KeyType": "RANGE"}
                ],
                "Projection": {"ProjectionType": "ALL"}
            }
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "SparePartsIQ-MaintenanceSchedules",
        "KeySchema": [{"AttributeName": "schedule_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [
            {"AttributeName": "schedule_id", "AttributeType": "S"},
            {"AttributeName": "machine_id", "AttributeType": "S"},
            {"AttributeName": "scheduled_date", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "MachineScheduleIndex",
                "KeySchema": [
                    {"AttributeName": "machine_id", "KeyType": "HASH"},
                    {"AttributeName": "scheduled_date", "KeyType": "RANGE"}
                ],
                "Projection": {"ProjectionType": "ALL"}
            }
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "SparePartsIQ-Suppliers",
        "KeySchema": [{"AttributeName": "supplier_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [
            {"AttributeName": "supplier_id", "AttributeType": "S"}
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "SparePartsIQ-PurchaseOrders",
        "KeySchema": [{"AttributeName": "po_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [
            {"AttributeName": "po_id", "AttributeType": "S"},
            {"AttributeName": "status", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "StatusIndex",
                "KeySchema": [{"AttributeName": "status", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"}
            }
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "SparePartsIQ-ForecastResults",
        "KeySchema": [
            {"AttributeName": "part_id", "KeyType": "HASH"},
            {"AttributeName": "forecast_horizon", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "part_id", "AttributeType": "S"},
            {"AttributeName": "forecast_horizon", "AttributeType": "S"}
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "SparePartsIQ-ReorderRecommendations",
        "KeySchema": [{"AttributeName": "recommendation_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [
            {"AttributeName": "recommendation_id", "AttributeType": "S"},
            {"AttributeName": "status", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "StatusIndex",
                "KeySchema": [{"AttributeName": "status", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"}
            }
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "SparePartsIQ-Notifications",
        "KeySchema": [{"AttributeName": "notification_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [
            {"AttributeName": "notification_id", "AttributeType": "S"},
            {"AttributeName": "recipient_role", "AttributeType": "S"},
            {"AttributeName": "created_at", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "RoleNotificationIndex",
                "KeySchema": [
                    {"AttributeName": "recipient_role", "KeyType": "HASH"},
                    {"AttributeName": "created_at", "KeyType": "RANGE"}
                ],
                "Projection": {"ProjectionType": "ALL"}
            }
        ],
        "BillingMode": "PAY_PER_REQUEST"
    }
]

def create_tables():
    existing_tables = set(dynamodb.list_tables()['TableNames'])
    print(f"Existing DynamoDB tables: {existing_tables}")
    
    for table_def in TABLES:
        name = table_def["TableName"]
        if name in existing_tables:
            print(f"Table '{name}' already exists.")
            continue
        print(f"Creating table '{name}'...")
        try:
            dynamodb.create_table(**table_def)
            print(f"Successfully initiated creation of table '{name}'")
        except Exception as e:
            print(f"Error creating table '{name}': {e}")
            
    print("Waiting for tables to be ACTIVE...")
    for table_def in TABLES:
        name = table_def["TableName"]
        while True:
            try:
                res = dynamodb.describe_table(TableName=name)
                status = res["Table"]["TableStatus"]
                if status == "ACTIVE":
                    print(f"Table '{name}' is ACTIVE.")
                    break
                print(f"Table '{name}' status: {status}, waiting...")
                time.sleep(2)
            except Exception as e:
                print(f"Waiting on '{name}': {e}")
                time.sleep(2)

if __name__ == "__main__":
    create_tables()

