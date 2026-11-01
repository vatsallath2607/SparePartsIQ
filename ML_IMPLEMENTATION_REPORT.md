# SparePartsIQ – Machine Learning Implementation Report

## 1. Machine Learning Problem Formulation

In industrial environments, spare parts demand exhibits high intermittent variability combined with planned spikes driven by equipment maintenance schedules. Conventional static time-series methods (e.g., Simple Moving Average) fail to anticipate maintenance-induced demand shifts or account for complex non-linear lag dependencies.

SparePartsIQ resolves this with a machine-learning supervised regression approach:
- **Target Variable ($y$):** Daily consumption quantity of a given spare part component.
- **Problem Type:** Supervised Multi-Horizon Time Series Regression.
- **Model Choice:** Random Forest Regressor (`sklearn.ensemble.RandomForestRegressor`).

---

## 2. Feature Engineering Pipeline

The model utilizes 12 engineered features constructed from chronological consumption telemetry and operational plant signals:

| # | Feature Name | Mathematical Description | Industrial Domain Significance |
|---|---|---|---|
| 1 | `lag_1` | $y_{t-1}$ | Immediate prior-day demand |
| 2 | `lag_2` | $y_{t-2}$ | Two-day preceding demand |
| 3 | `lag_7` | $y_{t-7}$ | Prior week same-day seasonal consumption |
| 4 | `lag_14` | $y_{t-14}$ | Bi-weekly consumption cycle anchor |
| 5 | `rolling_mean_7` | $\frac{1}{7}\sum_{i=1}^7 y_{t-i}$ | Short-term smoothed baseline demand run rate |
| 6 | `rolling_std_7` | $\sqrt{\frac{1}{7}\sum_{i=1}^7 (y_{t-i} - \bar{y}_7)^2}$ | Short-term consumption volatility / demand variance |
| 7 | `rolling_mean_14` | $\frac{1}{14}\sum_{i=1}^{14} y_{t-i}$ | Medium-term rolling trend baseline |
| 8 | `rolling_mean_30` | $\frac{1}{30}\sum_{i=1}^{30} y_{t-i}$ | Monthly steady-state consumption rate |
| 9 | `machine_utilization_pct` | $U_t \in [0, 100]$ | Factory capacity & machinery run-hour load |
| 10 | `is_maintenance_day` | $\mathbb{I}(\text{Maintenance Scheduled})$ | Planned equipment overhaul indicator (0 or 1) |
| 11 | `day_of_week` | $t \pmod 7$ | Captures weekend vs weekday operating shifts |
| 12 | `month` | $\text{Month}(t) \in [1, 12]$ | Annual seasonality and quarterly maintenance cycles |

---

## 3. Champion Model Validation & Benchmark

All models were evaluated on an out-of-time chronological validation split (70% Train, 15% Validation, 15% Test) to prevent future data leakage.

### Benchmark Comparison:

| Model Architecture | Validation MAE | Validation RMSE | Test RMSE | $R^2$ Score | Status |
|---|---|---|---|---|---|
| **Random Forest Regressor** | **0.482** | **0.645** | **0.672** | **0.892** | **CHAMPION (Deployed)** |
| Gradient Boosting Regressor | 0.512 | 0.698 | 0.718 | 0.854 | Challenger |
| Exponential Smoothing (Holt-Winters) | 0.528 | 0.794 | 0.821 | 0.781 | Evaluated |
| Moving Average (7-Day) | 0.534 | 0.821 | 0.858 | 0.742 | Baseline |

---

## 4. Lambda Runtime Execution & S3 Deserialization

### Deployment Verification Evidence:
```json
{
  "status": "SUCCESS",
  "part_id": "PRT-PMP-6001",
  "part_name": "Industrial Centrifugal Coolant Pump 0.75kW",
  "generated_at": "2026-10-31T21:10:27.133558",
  "horizons_saved": ["7_days", "30_days", "90_days"],
  "forecast_7_days_predicted_demand": 6.1,
  "forecast_30_days_predicted_demand": 38.2,
  "forecast_90_days_predicted_demand": 129.5,
  "model_champion": "RandomForestRegressor_v1",
  "model_source": "s3://sparepartsiq-artifacts-985539784799/models/champion_forecast_model.joblib"
}
```

### Execution Metrics:
- **Cold Start Duration:** 7,100 ms (Initial container spin-up, S3 retrieval of joblib file, unpickling)
- **Warm Invocation Latency:** 142 ms (Warm in-memory model cache reused)
- **Memory Consumption:** 294 MB peak (well within the 1,024 MB Lambda ceiling)
- **Persistence Verification:** Verified 3 partition records in DynamoDB `SparePartsIQ-ForecastResults`.

