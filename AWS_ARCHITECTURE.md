# SparePartsIQ – AWS Architecture Document

## 1. System Overview

SparePartsIQ is built on a serverless, event-driven cloud architecture on Amazon Web Services (AWS) in region `ap-south-1` (Mumbai). The application eliminates infrastructure management overhead, scales dynamically to workload spikes, and maintains strict adherence to a ₹0 (zero-cost) budget by utilizing AWS Free Tier allowances.

```
+-------------------------------------------------------------------------+
|                              USER BROWSER                               |
|                React + Vite Client (Single Page App)                    |
+-------------------------------------------------------------------------+
                                    |
                                    v HTTPS / REST
+-------------------------------------------------------------------------+
|                           AMAZON API GATEWAY                            |
|             REST API: SparePartsIQ-API (ID: ug4bzbni58)                 |
|             Stage: prod | Proxy Integration {proxy+}                    |
+-------------------------------------------------------------------------+
                                    |
                                    v AWS Lambda Proxy
+-------------------------------------------------------------------------+
|                            AWS LAMBDA                                   |
|             Function: SparePartsIQ-Backend (Python 3.12)                |
|             Handler: backend.main.handler (Mangum + FastAPI)            |
|             Memory: 1024 MB | Architecture: x86_64                      |
+-------------------------------------------------------------------------+
           |                             |                        |
           v                             v                        v
+-----------------------+   +------------------------+   +---------------+
|    AMAZON DYNAMODB    |   |       AMAZON S3        |   |   AMAZON SNS  |
| 9 Production Tables   |   | sparepartsiq-artifacts |   | SparePartsIQ- |
| * SpareParts          |   | -985539784799          |   | Alerts        |
| * Suppliers           |   |                        |   | (Topic Alert  |
| * Users               |   | ML Artifacts:          |   |  Publishing)  |
| * PurchaseOrders      |   | * models/champion_...  |   +---------------+
| * MaintenanceSchedules|   | * models/evaluation... |
| * InventoryTransactions|  | * datasets/historical..|
| * ForecastResults     |   | * lambda/backend_...   |
| * ReorderRecs         |   +------------------------+
| * Notifications       |
+-----------------------+
           ^
           | Scheduled Daily Trigger (02:00 UTC / 07:30 IST)
+-------------------------------------------------------------------------+
|                           AMAZON EVENTBRIDGE                            |
|                 Rule: SparePartsIQ-DailyForecastingRule                 |
|                 Target: Lambda Function SparePartsIQ-Backend            |
+-------------------------------------------------------------------------+
```

---

## 2. Resource Inventory & Configuration Details

### 2.1 Compute (AWS Lambda)
- **Function Name:** `SparePartsIQ-Backend`
- **ARN:** `arn:aws:lambda:ap-south-1:985539784799:function:SparePartsIQ-Backend`
- **Runtime:** Python 3.12 (`x86_64`)
- **Memory Allocation:** 1024 MB
- **Timeout:** 30 seconds
- **Handler:** `backend.main.handler`
- **Execution Role:** `arn:aws:iam::985539784799:role/SparePartsIQ-LambdaExecutionRole`
- **Active Environment Variables:**
  - `STORAGE_MODE`: `aws`
  - `S3_BUCKET`: `sparepartsiq-artifacts-985539784799`
  - `SNS_TOPIC_ARN`: `arn:aws:sns:ap-south-1:985539784799:SparePartsIQ-Alerts`
  - `TABLE_PARTS`: `SparePartsIQ-SpareParts`
  - `TABLE_FORECASTS`: `SparePartsIQ-ForecastResults`
  - `TABLE_USERS`: `SparePartsIQ-Users`

### 2.2 API Management (Amazon API Gateway)
- **API Name:** `SparePartsIQ-API`
- **API ID:** `ug4bzbni58`
- **Protocol:** REST API
- **Deployment Stage:** `prod`
- **Invoke Base URL:** `https://ug4bzbni58.execute-api.ap-south-1.amazonaws.com/prod`
- **Integration:** Proxy integration to `SparePartsIQ-Backend` for root and `{proxy+}` routes.
- **CORS Configuration:** `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Headers: *`, `Access-Control-Allow-Methods: *`.

### 2.3 Database (Amazon DynamoDB)
9 dedicated NoSQL tables configured with primary hash keys:

| Table Name | Primary Partition Key | Primary Sort Key |
|---|---|---|
| `SparePartsIQ-SpareParts` | `part_id` (String) | — |
| `SparePartsIQ-Suppliers` | `supplier_id` (String) | — |
| `SparePartsIQ-Users` | `email` (String) | — |
| `SparePartsIQ-PurchaseOrders` | `po_id` (String) | — |
| `SparePartsIQ-MaintenanceSchedules` | `schedule_id` (String) | — |
| `SparePartsIQ-InventoryTransactions` | `transaction_id` (String) | — |
| `SparePartsIQ-ForecastResults` | `part_id` (String) | `forecast_horizon` (String) |
| `SparePartsIQ-ReorderRecommendations` | `recommendation_id` (String) | — |
| `SparePartsIQ-Notifications` | `notification_id` (String) | — |

### 2.4 Object Storage (Amazon S3)
- **Bucket Name:** `sparepartsiq-artifacts-985539784799`
- **Region:** `ap-south-1`
- **Artifact Tree:**
  - `models/champion_forecast_model.joblib`: Trained Scikit-Learn Random Forest Regressor artifact.
  - `models/evaluation_report.json`: Historical model benchmark metrics comparing against Moving Average & Exponential Smoothing.
  - `datasets/historical_consumption.csv`: 24-month granular consumption log.
  - `lambda/backend_lambda.zip`: Deployment package containing application code, NumPy, SciPy, and Scikit-Learn wheels.

### 2.5 Scheduling & Notifications
- **EventBridge Rule:** `SparePartsIQ-DailyForecastingRule`
  - Schedule Expression: `cron(0 2 * * ? *)` (07:30 IST / 02:00 UTC daily)
  - Target: Lambda `SparePartsIQ-Backend`
- **SNS Topic:** `arn:aws:sns:ap-south-1:985539784799:SparePartsIQ-Alerts`
  - Used for publishing high-priority operational stockout and maintenance alerts.

