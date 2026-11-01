# SparePartsIQ – API Specification & Reference

**Base URL:** `https://ug4bzbni58.execute-api.ap-south-1.amazonaws.com/prod`  
**Authentication Scheme:** Bearer Token (JWT `Authorization: Bearer <access_token>`)  

---

## 1. System & Authentication Endpoints

### 1.1 Health Check
- **Route:** `GET /health` and `GET /api/health`
- **Auth:** None (Public)
- **Response:**
```json
{
  "status": "HEALTHY",
  "service": "SparePartsIQ-Backend",
  "mode": "aws",
  "region": "ap-south-1",
  "version": "1.0.0"
}
```

### 1.2 User Login
- **Route:** `POST /api/auth/login`
- **Auth:** None
- **Request:**
```json
{
  "email": "inventory@sparepartsiq.com",
  "password": "<configured_password>"
}
```
- **Response:**
```json
{
  "access_token": "<jwt_string>",
  "token_type": "bearer",
  "user": {
    "user_id": "USR-001",
    "name": "Vikramaditya Rao",
    "email": "inventory@sparepartsiq.com",
    "role": "Inventory Manager",
    "department": "Supply Chain & Warehouse"
  }
}
```

---

## 2. Inventory Management Endpoints

### 2.1 List Spare Parts
- **Route:** `GET /api/inventory`
- **Query Params:** `search`, `category`, `criticality`, `stock_status`
- **Auth:** Authenticated User

### 2.2 Create Spare Part
- **Route:** `POST /api/inventory`
- **Auth:** `Inventory Manager`, `Administrator`
- **Request:** Full part schema (`part_id`, `part_name`, `category`, `unit_cost`, `current_stock`, `reorder_point`, etc.)

### 2.3 Record Stock Transaction
- **Route:** `POST /api/inventory/{part_id}/transaction`
- **Auth:** Authenticated User
- **Request:**
```json
{
  "transaction_type": "IN",
  "quantity": 5,
  "reason": "Restock delivery from supplier"
}
```

---

## 3. AI Demand Forecasting Endpoints

### 3.1 List All Forecasts
- **Route:** `GET /api/forecasts`
- **Auth:** Authenticated User

### 3.2 Generate ML Forecast
- **Route:** `POST /api/forecasts/generate`
- **Auth:** Authenticated User
- **Request:**
```json
{
  "part_id": "PRT-PMP-6001",
  "horizon_days": 30
}
```
- **Response:**
```json
{
  "status": "SUCCESS",
  "part_id": "PRT-PMP-6001",
  "forecast_7_days_predicted_demand": 6.1,
  "forecast_30_days_predicted_demand": 38.2,
  "forecast_90_days_predicted_demand": 129.5,
  "model_champion": "RandomForestRegressor_v1",
  "model_source": "s3://sparepartsiq-artifacts-985539784799/models/champion_forecast_model.joblib"
}
```

### 3.3 Evaluation Metrics
- **Route:** `GET /api/forecasts/evaluation/metrics`
- **Auth:** Authenticated User
- **Source:** Loaded directly from S3 `models/evaluation_report.json`

---

## 4. Maintenance Planning Endpoints

### 4.1 List Machine Equipment
- **Route:** `GET /api/maintenance/machines`

### 4.2 List Maintenance Schedules
- **Route:** `GET /api/maintenance/schedules`

### 4.3 Detect At-Risk Schedules
- **Route:** `GET /api/maintenance/at-risk`
- **Logic:** Identifies equipment work orders where required spare parts stock is insufficient.

---

## 5. Stockout & Reorder Endpoints

### 5.1 Stockout Prediction Matrix
- **Route:** `GET /api/stockouts`
- **Route:** `GET /api/stockouts/summary`

### 5.2 Reorder Recommendations
- **Route:** `GET /api/reorders`
- **Route:** `POST /api/reorders/generate`
- **Route:** `POST /api/reorders/{id}/approve` (Requires `Purchase Manager`)
- **Route:** `POST /api/reorders/{id}/reject` (Requires `Purchase Manager`)

---

## 6. Purchase Orders & Suppliers

### 6.1 Purchase Orders
- **Route:** `GET /api/purchase-orders`
- **Route:** `POST /api/purchase-orders` (Requires `Purchase Manager`)
- **Route:** `PUT /api/purchase-orders/{id}/status` (Receiving stock updates inventory)

### 6.2 Suppliers
- **Route:** `GET /api/suppliers`
- **Route:** `POST /api/suppliers`

---

## 7. Executive Dashboard & Alerts

### 7.1 Dashboard KPIs
- **Route:** `GET /api/analytics/dashboard`

### 7.2 Notifications & Alerts
- **Route:** `GET /api/notifications`
- **Route:** `POST /api/notifications/alert` (Publishes to Amazon SNS topic)

