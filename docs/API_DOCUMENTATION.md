# SparePartsIQ REST API Documentation

The backend exposes a modular FastAPI REST API (compatible with AWS Lambda via Mangum).

Base URL: `http://localhost:8000` (or AWS API Gateway endpoint)

---

## 1. Authentication (`/api/auth`)

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/login` | Authenticate with email/password; returns JWT | Public |
| `GET` | `/api/auth/me` | Retrieve profile of authenticated user | Authenticated |
| `GET` | `/api/auth/users` | List active platform users | Authenticated |

---

## 2. Inventory Management (`/api/inventory`)

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/inventory` | List parts with search, category, criticality filters | Authenticated |
| `GET` | `/api/inventory/low-stock` | Retrieve parts below reorder point | Authenticated |
| `GET` | `/api/inventory/overstocked`| Retrieve parts exceeding max capacity | Authenticated |
| `GET` | `/api/inventory/{part_id}` | Retrieve single spare part specifications | Authenticated |
| `POST` | `/api/inventory` | Register new spare part in catalog | Inventory Manager |
| `PUT` | `/api/inventory/{part_id}` | Update existing spare part details | Inventory Manager |
| `DELETE`| `/api/inventory/{part_id}`| Delete spare part from catalog | Inventory Manager |
| `POST` | `/api/inventory/{part_id}/transaction` | Record movement (Restock, Consume, Adjust) | Authenticated |
| `GET` | `/api/inventory/{part_id}/transactions`| Retrieve transaction audit history | Authenticated |

---

## 3. AI Demand Forecasting (`/api/forecasts`)

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/forecasts` | List all forecasted parts with 7/30/90d horizons | Authenticated |
| `GET` | `/api/forecasts/{part_id}` | Retrieve forecast curves & historical series | Authenticated |
| `GET` | `/api/forecasts/evaluation/metrics` | Retrieve model benchmark comparison metrics | Authenticated |
| `POST` | `/api/forecasts/retrain` | Trigger model retraining pipeline in background | Inventory Manager |

---

## 4. Stockout Risk Prediction (`/api/stockouts`)

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/stockouts` | List stockout risk matrix with scores & reasons | Authenticated |
| `GET` | `/api/stockouts/summary` | Summary counts of Critical/High/Med/Low risks | Authenticated |

---

## 5. Reorder Recommendations (`/api/reorders`)

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/reorders` | List recommendations filtered by status | Authenticated |
| `POST` | `/api/reorders/{id}/approve` | Approve recommendation & auto-dispatch PO | Purchase Manager |
| `POST` | `/api/reorders/{id}/reject` | Reject recommendation with decision notes | Purchase Manager |

---

## 6. Maintenance Planning (`/api/maintenance`)

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/maintenance/machines` | List registered industrial machinery | Authenticated |
| `GET` | `/api/maintenance/schedules` | List upcoming maintenance schedules | Authenticated |
| `POST` | `/api/maintenance/schedules` | Register preventive/corrective work order | Maintenance Team |
| `GET` | `/api/maintenance/at-risk` | Identify maintenance tasks with part shortages | Authenticated |

---

## 7. Procurement & Suppliers (`/api/purchase-orders`, `/api/suppliers`)

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/purchase-orders` | List purchase orders with status filtering | Authenticated |
| `POST` | `/api/purchase-orders` | Issue manual purchase order | Purchase Manager |
| `PUT` | `/api/purchase-orders/{id}/status` | Update status (e.g., mark Received) | Purchase / Inventory |
| `GET` | `/api/suppliers` | List suppliers with ratings & lead times | Authenticated |
| `POST` | `/api/suppliers` | Register new certified supplier | Purchase Manager |

---

## 8. Dashboard & Notifications (`/api/analytics`, `/api/notifications`)

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/analytics/dashboard` | Executive KPIs, trends, category distributions | Authenticated |
| `GET` | `/api/notifications` | List alerts filtered by user role | Authenticated |
| `PUT` | `/api/notifications/{id}/read` | Mark notification as read | Authenticated |
| `POST` | `/api/notifications/alert` | Trigger high-priority alert (DynamoDB & SNS) | Authenticated |
| `GET` | `/api/health` | Healthcheck and service version status | Public |

