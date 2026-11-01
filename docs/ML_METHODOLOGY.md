# SparePartsIQ Machine Learning Methodology & Evaluation

## 1. Problem Framing
Industrial spare parts demand exhibits intermittent, "lumpy" characteristics driven by machine operational hours, cyclic preventive maintenance, and component lifecycle limits.

Traditional time-series models often fail by either overreacting to sporadic spikes or underestimating inventory required during planned maintenance overhauls.

---

## 2. Dataset Strategy
A synthetic yet mathematically grounded industrial dataset was generated covering **3,650 daily observation records** across 10 critical industrial spare parts over a 365-day observation window.

The dataset models:
- **Baseline Intermittent Demand:** Generated via Poisson arrival processes parameterized by component category run rates.
- **Maintenance Schedule Demand Spikes:** Periodic overhaul pulses matching multi-unit maintenance schedules.
- **Machine Utilization:** Telemetry factors reflecting factory operational tempos (weekdays 70–96%, weekend shift reductions 40–65%).
- **Annual Cyclical Seasonality:** Mid-year overhaul waves modeled via sinusoidal factors.

---

## 3. Feature Engineering Pipeline
Each observation is enriched with 12 features:

| Feature Name | Type | Description |
| :--- | :--- | :--- |
| `lag_1` | Numeric | Prior day consumption ($t-1$) |
| `lag_2` | Numeric | Two days prior consumption ($t-2$) |
| `lag_7` | Numeric | Weekly cycle lag ($t-7$) |
| `lag_14` | Numeric | Bi-weekly cycle lag ($t-14$) |
| `rolling_mean_7` | Numeric | 7-day rolling average consumption |
| `rolling_std_7` | Numeric | 7-day rolling demand volatility ($\sigma$) |
| `rolling_mean_14` | Numeric | 14-day rolling average consumption |
| `rolling_mean_30` | Numeric | 30-day baseline moving average |
| `machine_utilization_pct` | Percentage | Machine operational workload |
| `is_maintenance_day` | Binary | Scheduled overhaul event indicator |
| `day_of_week` | Categorical | Day of week indicator (0=Mon ... 6=Sun) |
| `month` | Categorical | Calendar month factor |

---

## 4. Chronological Train-Val-Test Splitting
To ensure strict avoidance of lookahead bias and data leakage:
- **Training Set (70%):** Earliest 255 consecutive chronological days.
- **Validation Set (15%):** Next 55 consecutive chronological days.
- **Test Set (15%):** Final 55 consecutive chronological days (out-of-sample).

---

## 5. Model Candidate Comparison

Four models were trained and benchmarked using standard regression metrics:
- **Mean Absolute Error (MAE):** Average magnitude of forecast error.
- **Root Mean Squared Error (RMSE):** Penalizes large deviations, critical for industrial safety stocks.
- **Mean Absolute Percentage Error (MAPE):** Relative percentage deviation on positive consumption days.

### Evaluation Benchmark Results

| Model | Val MAE | Val RMSE | Test MAE | Test RMSE | Test MAPE (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Simple Moving Average (7D)** | 0.5340 | 0.8209 | 0.5558 | 0.8583 | 75.54% |
| **Exponential Smoothing ($\alpha=0.3$)** | 0.6771 | 0.8383 | 0.6815 | 0.8606 | 46.25% |
| **Random Forest Regressor** | **0.4908** | **0.6451** | **0.4802** | **0.6155** | 59.13% |
| **Gradient Boosting Regressor** | 0.5052 | 0.6724 | 0.4777 | 0.6165 | 59.30% |

### Champion Model Selection
The **Random Forest Regressor** achieved the lowest Validation RMSE (`0.6451`) and Test RMSE (`0.6155`), achieving a **28.3% error reduction** compared to the Moving Average baseline.

---

## 6. Model Serialization & Cloud Deployment
- **Artifact:** Serialized using `joblib` into `champion_forecast_model.joblib`.
- **Cloud Storage:** Uploaded to Amazon S3 at:
  `s3://sparepartsiq-artifacts-985539784799/models/champion_forecast_model.joblib`
- **Evaluation Report:** Uploaded to Amazon S3 at:
  `s3://sparepartsiq-artifacts-985539784799/models/evaluation_report.json`

