import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv(override=True)

# STORAGE CONFIGURATION
# Default to "aws" for live cloud demonstration. Set to "sqlite" only for offline testing.
STORAGE_MODE = os.getenv("STORAGE_MODE", "aws")

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", None)
S3_BUCKET = os.getenv("S3_BUCKET", "sparepartsiq-artifacts-985539784799")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "arn:aws:sns:ap-south-1:985539784799:SparePartsIQ-Alerts")

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError(
        "CRITICAL SECURITY CONFIGURATION ERROR: JWT_SECRET environment variable is missing or empty. "
        "A secure, cryptographically random secret must be configured in environment variables."
    )
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60 * 24  # 24 hours

# DynamoDB Tables (used in AWS mode)
TABLE_USERS = os.getenv("TABLE_USERS", "SparePartsIQ-Users")
TABLE_PARTS = os.getenv("TABLE_PARTS", "SparePartsIQ-SpareParts")
TABLE_TRANSACTIONS = os.getenv("TABLE_TRANSACTIONS", "SparePartsIQ-InventoryTransactions")
TABLE_MAINTENANCE = os.getenv("TABLE_MAINTENANCE", "SparePartsIQ-MaintenanceSchedules")
TABLE_SUPPLIERS = os.getenv("TABLE_SUPPLIERS", "SparePartsIQ-Suppliers")
TABLE_POS = os.getenv("TABLE_POS", "SparePartsIQ-PurchaseOrders")
TABLE_FORECASTS = os.getenv("TABLE_FORECASTS", "SparePartsIQ-ForecastResults")
TABLE_REORDERS = os.getenv("TABLE_REORDERS", "SparePartsIQ-ReorderRecommendations")
TABLE_NOTIFICATIONS = os.getenv("TABLE_NOTIFICATIONS", "SparePartsIQ-Notifications")
