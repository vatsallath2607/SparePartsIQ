# SparePartsIQ – Live Faculty Demonstration Script

This document provides a guided walkthrough for presenting SparePartsIQ.

---

## 1. Demo Credentials & Quick Login

Navigate to `http://localhost:3000/login`

> [!NOTE]
> Passwords are configured during database setup via `python scripts/seed_dynamodb.py` or `python scripts/seed_sqlite.py`. During local deployment, seed credentials match the environment configuration.

| Role | Email | Password | Primary Demonstration Focus |
|---|---|---|---|
| **Inventory Manager** | `inventory@sparepartsiq.com` | `[Configured at seed time]` | Catalog, Stock Adjustments, AI Demand Forecasting |
| **Maintenance Team** | `maintenance@sparepartsiq.com` | `[Configured at seed time]` | Equipment Overhauls, Work Orders, At-Risk Deficit Detection |
| **Purchase Manager** | `purchase@sparepartsiq.com` | `[Configured at seed time]` | Reorder Proposals Approval, PO Issuance, Delivery Receiving |

---

## 2. Step-by-Step Demonstration Walkthrough

### Step 1: Executive Analytics Dashboard (`/`)
- Point out real-time KPI cards: **Spare Parts (65)**, **Inventory Valuation ($5.9M+)**, **Low Stock (30)**.
- Highlight the **Asset Valuation by Category** chart showing capital distribution.
- Show **Consumption Trends** reflecting monthly factory usage.
- Point to **Top Attention Components** highlighting items below ROP.

### Step 2: AI Demand Forecasting (`/forecasting`)
- Select spare part: `High Precision Spindle Bearing (PRT-BRG-1001)` or `Coolant Pump (PRT-PMP-6001)`.
- Toggle forecast horizon: **7 Days**, **30 Days**, **90 Days**.
- Explain that the values represent **genuine Random Forest ML predictions** loaded from S3 and executed inside AWS Lambda.
- Point out the **Historical Consumption vs. Machine Learning Forecast Projection** chart.

### Step 3: Model Evaluation & Benchmarks (`/model-evaluation`)
- Show the live evaluation report retrieved from S3.
- Explain the champion model selection:
  - **Random Forest Regressor** achieved RMSE of `0.6451` and $R^2$ of `0.892`, beating Moving Average (`0.8209`) and Exponential Smoothing (`0.794`).
- Review the 12 engineered features including lag variables, rolling volatility, and scheduled maintenance indicators.

### Step 4: Maintenance-Based Inventory Planning (`/maintenance`)
- View **Scheduled Work Orders** for CNC milling machines, turbines, and presses.
- Switch to the **At-Risk Activities** tab to demonstrate cross-referencing between equipment overhauls and stock levels.

### Step 5: Stockout Risk Prediction Matrix (`/stockouts`)
- Review parts categorized by risk tier: **Critical**, **High**, **Medium**, and **Low**.
- Filter by **High Risk** to show parts where days of supply is lower than supplier lead time.

### Step 6: Automated Reorder Engine (`/reorder`)
- Switch user role to **Purchase Manager** via the role switcher in the navbar.
- Review AI-generated reorder proposals.
- Click **Approve & Dispatch PO** on a proposal.
- Observe instant conversion to a live Purchase Order with automated delivery calculation based on supplier lead times.

### Step 7: Purchase Orders & Receiving (`/purchase-orders`)
- Locate the newly approved Purchase Order.
- Click **Mark Received**.
- Confirm that inventory stock in `SparePartsIQ-SpareParts` is updated in DynamoDB.

