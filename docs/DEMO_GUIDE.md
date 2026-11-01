# SparePartsIQ Project Demonstration Guide

This guide walks through testing and evaluating all 8 core modules of the live SparePartsIQ application.

---

## 1. Accessing the Live Application

- **Frontend URL:** `http://localhost:3000`
- **Backend API & OpenAPI Docs:** `http://localhost:8000/docs`
- **Healthcheck:** `http://localhost:8000/api/health`

---

## 2. Test User Accounts & Roles

The application includes built-in 1-click role buttons on the login screen and a top-bar switcher for fast evaluation:

| Role | Email | Password | Primary Capabilities |
| :--- | :--- | :--- | :--- |
| **Inventory Manager** | `inventory@sparepartsiq.com` | `[Configured at seed time]` | Add/Edit spare parts, check-in/consume stock, trigger ML retraining |
| **Maintenance Team** | `maintenance@sparepartsiq.com` | `[Configured at seed time]` | Schedule maintenance, inspect required parts & shortages |
| **Purchase Manager** | `purchase@sparepartsiq.com` | `[Configured at seed time]` | Approve/Reject reorders, issue POs, mark received |

---

## 3. Step-by-Step Demonstration Workflow

### Step 1: Executive Dashboard
1. Open `http://localhost:3000/`.
2. Inspect the 6 high-level KPI cards (Total Spare Parts, Asset Valuation, Low Stock Items, Critical Stockouts, Upcoming Maintenance, Pending Reorders).
3. Review the interactive **Consumption & Expenditure Trend** area chart and **Asset Valuation by Category** bar chart.

### Step 2: Inventory Catalog & Stock Movements
1. Navigate to **Inventory Catalog** (`/inventory`).
2. Test searching for "Bearing" or filtering by category "Mechanical & Bearings" or criticality "Critical".
3. Click the stock adjustment icon on any item:
   - Perform a **Consume (OUT)** transaction to decrease stock.
   - Notice the inventory count immediately updates and records an audit log.

### Step 3: AI Demand Forecasting
1. Navigate to **AI Demand Forecast** (`/forecasting`).
2. Select any spare part from the dropdown.
3. Toggle between **7 Days**, **30 Days**, and **90 Days** forecast horizons.
4. Review the timeline chart combining 30-day historical actual consumption with the 30-day forward ML projection curve.
5. Click **Trigger ML Retraining** to demonstrate background retraining and artifact update.

### Step 4: Stockout Risk Matrix
1. Navigate to **Stockout Risk Matrix** (`/stockouts`).
2. Click the summary filter buttons (**Critical Risk**, **High Risk**, **Medium Risk**, **Low Risk**).
3. Review the diagnostic reason column detailing why a component is classified at risk (e.g. coverage days vs supplier lead time).

### Step 5: Intelligent Reorder Engine
1. Switch to **Purchase Manager** using the top-right role switcher or login screen.
2. Navigate to **Reorder Engine** (`/reorder`).
3. Inspect the recommended order quantities, calculated ROP, and safety stock.
4. Click **Approve & Dispatch PO** on any pending recommendation.
5. Enter optional approval notes; verify the recommendation status changes to `Approved` and a Purchase Order is automatically generated.

### Step 6: Maintenance Planning & Deficit Alerts
1. Navigate to **Maintenance Planning** (`/maintenance`).
2. Switch to the **At-Risk Activities** tab to view work orders threatened by component stockouts.
3. Click **Schedule Maintenance** to add a work order for a 5-Axis CNC machine or Turbine Generator.

### Step 7: Purchase Orders & Automated Replenishment
1. Navigate to **Purchase Orders** (`/purchase-orders`).
2. Locate an open PO with status `Ordered` or `In-Transit`.
3. Click **Mark Received**; verify that the status transitions to `Received` and the corresponding spare part stock in the inventory catalog is immediately replenished.

### Step 8: ML Model Benchmark
1. Navigate to **ML Model Evaluation** (`/model-evaluation`).
2. Review the chronological 70/15/15 train/val/test split methodology.
3. Inspect the comparison table showing MAE, RMSE, and MAPE across Moving Average, Exponential Smoothing, Random Forest, and Gradient Boosting.

