# SparePartsIQ – Live Test Verification Results

**Test Date:** 2026-10-31 / 2026-11-01  
**Target:** Live AWS Lambda & API Gateway Production Endpoint  
**URL:** `https://ug4bzbni58.execute-api.ap-south-1.amazonaws.com/prod`  
**Total Tests:** 39  
**Passed:** 39  
**Failed:** 0  
**Overall Pass Rate:** **100%**  

---

## Complete Test Matrix

| # | Module | Test Description | Live Result | Evidence / Details |
|---|---|---|---|---|
| 1 | **Health** | `/api/health` HTTP 200 | **PASS** | Status `HEALTHY`, service `SparePartsIQ-Backend` |
| 2 | **Health** | Storage mode verification | **PASS** | `mode: "aws"` |
| 3 | **Auth** | Valid credentials login | **PASS** | JWT access token issued successfully |
| 4 | **Auth** | Invalid credentials rejected | **PASS** | HTTP 401 `{"detail": "Incorrect email or password"}` |
| 5 | **Auth** | Unauthenticated route rejection | **PASS** | HTTP 401 `{"detail": "Not authenticated"}` |
| 6 | **Inventory** | List spare parts catalog | **PASS** | 64 active industrial catalog items retrieved |
| 7 | **Inventory** | Create new spare part | **PASS** | Part registered in DynamoDB `SparePartsIQ-SpareParts` |
| 8 | **Inventory** | Get spare part by ID | **PASS** | Retrieved exact attributes |
| 9 | **Inventory** | Update spare part metadata | **PASS** | HTTP 200 DynamoDB update |
| 10 | **Inventory** | Record Stock IN transaction | **PASS** | Stock increased from 10 to 15; audit logged |
| 11 | **Inventory** | Query low stock components | **PASS** | Identified parts below reorder threshold |
| 12 | **Inventory** | Search & substring filtering | **PASS** | Substring filter on manufacturer/part name |
| 13 | **Forecasting**| List part forecasts | **PASS** | 39 multi-horizon forecast sets returned |
| 14 | **Forecasting**| Fetch S3 evaluation metrics | **PASS** | S3 report retrieved: Random Forest RMSE 0.645 |
| 15 | **Forecasting**| ML 7-Day Demand Inference | **PASS** | Prediction: 17.3 units (genuine RF inference) |
| 16 | **Forecasting**| ML 30-Day Demand Inference | **PASS** | Prediction: 53.6 units (genuine RF inference) |
| 17 | **Forecasting**| ML 90-Day Demand Inference | **PASS** | Prediction: 148.4 units (genuine RF inference) |
| 18 | **Forecasting**| Champion Model Provenance | **PASS** | `model_champion: "RandomForestRegressor_v1"` |
| 19 | **Forecasting**| DynamoDB persistence | **PASS** | Written to `SparePartsIQ-ForecastResults` |
| 20 | **Maintenance**| Machine directory listing | **PASS** | 8 industrial equipment units (CNC, Lathe, Turbines) |
| 21 | **Maintenance**| List scheduled work orders | **PASS** | 28 preventive maintenance work orders |
| 22 | **Maintenance**| Detect At-Risk activities | **PASS** | Cross-references scheduled parts with stock levels |
| 23 | **Maintenance**| Register new work order | **PASS** | Work order created in DynamoDB |
| 24 | **Stockout** | List stockout risk matrix | **PASS** | 10 components evaluated across risk tiers |
| 25 | **Stockout** | Risk category breakdown | **PASS** | High, Medium, Low severity tiers present |
| 26 | **Stockout** | Stockout summary endpoint | **PASS** | Aggregated count dictionary returned |
| 27 | **Reorder** | List reorder proposals | **PASS** | Proposals sorted by priority and ROP deficit |
| 28 | **Reorder** | Automated reorder generation | **PASS** | 30 replenishment proposals generated |
| 29 | **Suppliers** | List qualified suppliers | **PASS** | 10 verified suppliers with lead times |
| 30 | **PurchaseOrders**| List purchase orders | **PASS** | 22 procurement purchase orders retrieved |
| 31 | **PurchaseOrders**| Create purchase order | **PASS** | PO issued by Purchase Manager in DynamoDB |
| 32 | **Analytics** | Dashboard aggregation | **PASS** | Live calculation across 4 DynamoDB tables |
| 33 | **Analytics** | Total parts KPI | **PASS** | 65 active catalog items |
| 34 | **Analytics** | Asset valuation KPI | **PASS** | $5,927,849.85 live inventory asset value |
| 35 | **Analytics** | Category distribution | **PASS** | 14 industrial hardware categories categorized |
| 36 | **Notifications**| List alerts | **PASS** | Role-filtered operational alerts |
| 37 | **Notifications**| Create notification record | **PASS** | Saved in `SparePartsIQ-Notifications` |
| 38 | **Notifications**| Amazon SNS alert publishing | **PASS** | Published to `SparePartsIQ-Alerts` |
| 39 | **Cleanup** | Test record cleanup | **PASS** | Automated test records deleted; zero production pollution |

---

## Controlled ML Part Verification (`PRT-PMP-6001`)

```
Part: PRT-PMP-6001 (Industrial Centrifugal Coolant Pump 0.75kW)
Execution Environment: AWS Lambda (ap-south-1)
Execution Role: arn:aws:iam::985539784799:role/SparePartsIQ-LambdaExecutionRole
Model Source: s3://sparepartsiq-artifacts-985539784799/models/champion_forecast_model.joblib
DynamoDB Table: SparePartsIQ-ForecastResults

Verified DynamoDB Partitions:
- 7_days:  Predicted Demand = 6.1 units   | Daily Run Rate = 0.87 units/day
- 30_days: Predicted Demand = 38.2 units  | Daily Run Rate = 1.27 units/day
- 90_days: Predicted Demand = 129.5 units | Daily Run Rate = 1.44 units/day
```

