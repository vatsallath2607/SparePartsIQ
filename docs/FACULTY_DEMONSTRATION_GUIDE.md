# SparePartsIQ — Final Faculty Demonstration & Review Guide

**Project Name:** SparePartsIQ – AI-Powered Industrial Spare Parts Inventory Intelligence & Predictive Optimization Platform  
**Target AWS Account:** `985539784799`  
**Target Region:** `ap-south-1` (Mumbai)  
**Storage Architecture:** Dual-Engine (Live Amazon DynamoDB + S3, with 100% Zero-Cost Local SQLite Fallback)  
**Budget Consumed:** **INR 0.00**

---

## 1. Executive Summary for Evaluators

SparePartsIQ addresses one of the most persistent operational bottlenecks in modern manufacturing: **unplanned machine downtime caused by spare parts stockouts versus excessive inventory holding costs.**

Traditional Enterprise Resource Planning (ERP) systems rely on static Minimum/Maximum thresholds that fail to account for machine health degradation, seasonal consumption swings, or volatile supplier lead times. SparePartsIQ solves this by unifying:
1. **Machine Learning Demand Forecasting:** Multi-horizon demand prediction (7-day, 30-day, 90-day) using a champion Random Forest model ($R^2 = 0.892$, $\text{RMSE} = 0.645$).
2. **Dynamic Reorder Point (ROP) Optimization:** Real-time calculation based on safety stock, supplier lead times, and scheduled preventive maintenance requirements.
3. **AWS Cloud Integration:** Amazon DynamoDB for ultra-low latency NoSQL catalog storage, Amazon S3 for ML model artifact management, Amazon EventBridge for scheduled cron evaluation, and Amazon SNS for automated critical alerts.

---

## 2. Step-by-Step Demonstration Walkthrough

Follow this exact 9-step demonstration during your final project review:

### Step 1: Frontend Industrial SaaS Dashboard
* **Action:** Open your browser to `http://localhost:3000`
* **Observations to highlight to Faculty:**
  * **Status Indicator:** Shows `AWS CONNECTED (ap-south-1)` in green, verified via live backend health check (`/api/health`).
  * **Executive KPIs:** Live counts from DynamoDB showing Total Spare Parts (59 items), Total Inventory Value, Low-Stock Alerts, and Active Reorder Triggers.
  * **Role Switcher:** Rapidly switch between `Inventory Manager` (Vikramaditya Rao), `Maintenance Team` (Suresh Sen), and `Purchase Manager` (Meera Kulkarni) to demonstrate Role-Based Access Control (RBAC).

---

### Step 2: Amazon S3 — Machine Learning Artifact Store
* **Action:** Navigate to [AWS S3 Console](https://s3.console.aws.amazon.com/s3/buckets/sparepartsiq-artifacts-985539784799?region=ap-south-1)
* **Objects to show:**
  1. `datasets/historical_consumption.csv` (410 KB) — 3,650 daily industrial consumption records across machines and components.
  2. `models/champion_forecast_model.joblib` (651 KB) — Serialized scikit-learn Random Forest model.
  3. `models/evaluation_report.json` — Rigorous benchmark comparing 4 candidate algorithms across chronological train/val/test splits.
* **Talking Point:** *"The ML pipeline trains offline on historical machine consumption, serializes the champion model to S3, and loads it for low-latency batch and on-demand inference."*

---

### Step 3: Amazon DynamoDB — Real Industrial Records
* **Action:** Navigate to [AWS DynamoDB Tables Console](https://ap-south-1.console.aws.amazon.com/dynamodbv2/home?region=ap-south-1#tables)
* **Verified Tables and Record Counts:**
  * **`SparePartsIQ-SpareParts` (59 items):** Industrial catalog with dual-key schema, criticality ratings, and dynamic ROPs.
  * **`SparePartsIQ-Suppliers` (10 items):** SKF India, Bosch Rexroth, Festo, Siemens, Parker Hannifin, Timken, etc.
  * **`SparePartsIQ-InventoryTransactions` (200 items):** Historical IN, OUT, and AUDIT inventory movements.
  * **`SparePartsIQ-MaintenanceSchedules` (25 items):** Overdue and upcoming machine servicing schedules.
  * **`SparePartsIQ-PurchaseOrders` (19 items):** Industrial procurement orders linked to suppliers and parts.
  * **`SparePartsIQ-ForecastResults` (114 items):** 7d, 30d, and 90d demand forecasts.
  * **`SparePartsIQ-ReorderRecommendations` (53 items):** Algorithmic reorder triggers with dynamic safety stocks.
  * **`SparePartsIQ-Notifications` (14 items):** Real-time stockout risk alerts.
  * **`SparePartsIQ-Users` (4 items):** Bcrypt-hashed enterprise credentials.

---

### Step 4: Live End-to-End Proof (The Key Demonstration)
Demonstrate live write and read across the cloud stack:

1. **Add a New Part in Frontend:**
   * Go to **Inventory** page -> Click **Add Spare Part**.
   * Enter:
     * Name: `High-Torque Planetary Gearbox 50:1`
     * Category: `Power Transmission`
     * Stock: `4` | Min: `5` | ROP: `8` | Max: `20`
     * Price: `₹45,000`
   * Click **Save Spare Part**.
2. **Verify in AWS DynamoDB Console:**
   * Open `SparePartsIQ-SpareParts` in DynamoDB Console -> Click **Explore Items**.
   * Run Scan or search by Part ID.
   * **Show the newly created item sitting in AWS DynamoDB in real-time.**
3. **Generate Forecast:**
   * Go to **Demand Forecasting** page -> Click **Generate ML Forecast**.
   * Show the 30-day predicted consumption curve and confidence interval ($[\text{Lower}, \text{Upper}]$).
   * Open `SparePartsIQ-ForecastResults` in AWS DynamoDB to show the saved forecast record.

---

### Step 5: Machine Learning & Reorder Recommendation Engine
* **Action:** Go to **Reorder Recommendations** page
* **Explain the Formula:**
  $$\text{Reorder Point (ROP)} = (\text{Avg Daily Demand} \times \text{Supplier Lead Time}) + \text{Safety Stock} + \text{Maintenance Demand}$$
* **Show Workflow:**
  * Highlight recommendation `REC-GEN-PRT-ELC-4001` flagged as `URGENT`.
  * Click **Approve Recommendation** as Purchase Manager.
  * Show that it automatically creates a corresponding Purchase Order in `SparePartsIQ-PurchaseOrders` in DynamoDB.

---

### Step 6: Amazon EventBridge — Automated Daily Forecasting
* **Action:** Navigate to [AWS EventBridge Rules Console](https://ap-south-1.console.aws.amazon.com/events/home?region=ap-south-1#/rules)
* **Show:**
  * Rule: `SparePartsIQ-DailyForecastingRule`
  * State: `ENABLED`
  * Schedule Expression: `cron(0 2 * * ? *)` (Runs daily at 02:00 UTC / 07:30 IST).
  * Purpose: Triggers autonomous daily inventory health evaluation and stockout risk assessment without human intervention.

---

### Step 7: Amazon SNS — Alert Notification Topic
* **Action:** Navigate to [AWS SNS Topics Console](https://ap-south-1.console.aws.amazon.com/sns/v3/home?region=ap-south-1#/topics)
* **Show:**
  * Topic ARN: `arn:aws:sns:ap-south-1:985539784799:SparePartsIQ-Alerts`
  * Explain: High-severity stockout events and overdue machine servicing alerts publish notifications to this topic for plant manager SMS/Email distribution.

---

## 3. Machine Learning Benchmark Results

| Model | Validation MAE | Validation RMSE | Test RMSE | $R^2$ Score | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Random Forest Regressor** | **0.4908** | **0.6451** | **0.6155** | **0.892** | 🏆 **Champion** |
| Gradient Boosting Regressor | 0.5052 | 0.6724 | 0.6165 | 0.884 | Challenger |
| Moving Average (7-Day) | 0.5340 | 0.8209 | 0.8583 | 0.741 | Baseline |
| Exponential Smoothing ($\alpha=0.3$) | 0.6771 | 0.8383 | 0.8606 | 0.728 | Baseline |

---

## 4. How to Run the Application

```powershell
# 1. Start Backend in AWS Mode
$env:STORAGE_MODE = "aws"
$env:AWS_PROFILE = "antigravity-project"
$env:AWS_REGION = "ap-south-1"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# 2. In another terminal, start Frontend
cd frontend
npm run dev
# Opens at http://localhost:3000
```

### Pre-configured Login Accounts:
* **Inventory Manager:** `inventory@sparepartsiq.com` | `[Configured at seed time]`
* **Purchase Manager:** `purchase@sparepartsiq.com` | `[Configured at seed time]`
* **Maintenance Team:** `maintenance@sparepartsiq.com` | `[Configured at seed time]`
* **Administrator:** `admin@sparepartsiq.com` | `[Configured at seed time]`

