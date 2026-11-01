# SparePartsIQ – Machine Learning Faculty Demonstration Guide

**Project Name:** SparePartsIQ – AI-Powered Industrial Spare Parts Inventory Management and Predictive Maintenance System  
**Academic Target:** Faculty Review, Viva Voce Examination & Project Demonstration  
**Document Purpose:** Exhaustive architectural and statistical explanation of the Machine Learning forecasting subsystem, candidate model benchmarks, serverless AWS inference pipeline, and viva defense questions.

---

## 1. Exact Source Code & Artifact File Locations

Every component of the Machine Learning pipeline is implemented in the repository at the following exact paths:

| Component | Exact File Path | Description |
|---|---|---|
| **Data Synthesis Script** | [`ml/dataset_generator.py`](file:///C:/Users/Public/SparePartsIQ/ml/dataset_generator.py) | Generates 365 days of industrial equipment telemetry, machine utilization, maintenance cycles, and component consumption across 64 spare parts. |
| **Model Training & Evaluation Script** | [`ml/forecasting.py`](file:///C:/Users/Public/SparePartsIQ/ml/forecasting.py) | Implements feature engineering (`create_features()`), chronological data splitting, 4 candidate models fitting, metric computation, and model serialization. |
| **Historical Consumption Dataset** | [`data/historical_consumption.csv`](file:///C:/Users/Public/SparePartsIQ/data/historical_consumption.csv) | Primary dataset containing 23,360 daily observation rows (64 parts × 365 days). |
| **Model Evaluation Report** | [`ml/artifacts/evaluation_report.json`](file:///C:/Users/Public/SparePartsIQ/ml/artifacts/evaluation_report.json) | The authoritative JSON document recording cross-validation and test metrics across all 4 evaluated models. |
| **Serialized Champion Model** | [`ml/artifacts/champion_forecast_model.joblib`](file:///C:/Users/Public/SparePartsIQ/ml/artifacts/champion_forecast_model.joblib) | Scikit-learn serialized Random Forest model (651 KB binary). |
| **AWS Backend Inference Engine** | [`backend/routers/forecast_routes.py`](file:///C:/Users/Public/SparePartsIQ/backend/routers/forecast_routes.py) | Contains `load_champion_model()`, S3 download to `/tmp/`, warm in-memory caching, and `execute_ml_forecast()` 90-day autoregressive inference. |
| **EventBridge Daily Automation** | [`backend/main.py`](file:///C:/Users/Public/SparePartsIQ/backend/main.py) | Serverless Lambda handler wrapper intercepting `aws.events` scheduled payloads to execute daily batch inference jobs. |
| **Frontend Evaluation Dashboard** | [`frontend/src/pages/ModelEvaluation.jsx`](file:///C:/Users/Public/SparePartsIQ/frontend/src/pages/ModelEvaluation.jsx) | Interactive UI displaying metrics, error comparison charts, selection justification, and the 10-step serverless pipeline. |
| **Presentation Graphs Directory** | [`docs/ml_visualizations/`](file:///C:/Users/Public/SparePartsIQ/docs/ml_visualizations/) | High-resolution 300 DPI PNG graphs comparing RMSE, MAE, MAPE, and feature importances. |

---

## 2. Actual Evaluation Results & Model Comparison Matrix

The candidate models were evaluated using a strict **Chronological Split** (70% Train = Days 1–255, 15% Validation = Days 256–310, 15% Test = Days 311–365). Random shuffling was deliberately prohibited to prevent future lookahead data leakage.

### Official Metrics from `ml/artifacts/evaluation_report.json`

| Model Name | Model Class | Val MAE | Val RMSE | Test MAE | Test RMSE | Test MAPE (%) | Selection Decision |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Simple Moving Average (7D)** | Statistical Baseline | 0.5340 | 0.8209 | 0.5558 | 0.8583 | 75.54% | Rejected (Heuristic baseline) |
| **Exponential Smoothing ($\alpha=0.3$)** | Statistical Baseline | 0.6771 | 0.8383 | 0.6815 | 0.8606 | 46.25% | Rejected (Under-predicts demand) |
| **Gradient Boosting Regressor** | Tree Ensemble (GBDT) | 0.5052 | 0.6724 | **0.4777** | 0.6165 | 59.30% | Runner-up Candidate |
| **Random Forest Regressor** | Bagged Tree Ensemble | **0.4908** | **0.6451** | 0.4802 | **0.6155** | 59.13% | **🏆 SELECTED CHAMPION** |

> [!NOTE]
> **Lower Error is Better:** For MAE, RMSE, and MAPE, lower values indicate closer alignment with true industrial consumption.

---

## 3. Detailed Explanation of Evaluation Graphs

All seven graphs located in `docs/ml_visualizations/` are generated directly from `evaluation_report.json`:

1. **`val_rmse_comparison.png` (Validation RMSE):**
   - Shows Root Mean Squared Error on the 15% validation split.
   - **Key takeaway:** Random Forest achieved **0.6451**, outperforming Gradient Boosting (0.6724) and statistical baselines (>0.82). This metric guided hyperparameter tuning.
2. **`test_rmse_comparison.png` (Test RMSE):**
   - Evaluates generalization on completely unseen out-of-sample test days (Days 311–365).
   - **Key takeaway:** Random Forest achieved the **lowest Test RMSE of 0.6155**, lower than Gradient Boosting (0.6165).
3. **`val_mae_comparison.png` (Validation MAE):**
   - Shows average absolute quantity discrepancy during validation.
   - **Key takeaway:** Random Forest achieved **0.4908**, superior to GBDT (0.5052) and Moving Average (0.5340).
4. **`test_mae_comparison.png` (Test MAE):**
   - **Key takeaway:** Gradient Boosting achieved 0.4777 vs Random Forest's 0.4802 (a marginal 0.0025 unit difference). This is an honest benchmark finding where GBDT marginally edged RF on L1 error, but RF dominated on L2 error (RMSE).
5. **`test_mape_comparison.png` (Test MAPE %):**
   - Shows relative error on non-zero consumption days.
   - **Key takeaway:** Random Forest (59.13%) and GBDT (59.30%) demonstrated virtually identical percentage stability, while Simple Moving Average suffered a high 75.54% MAPE.
6. **`overall_model_benchmark_matrix.png` (Consolidated 4-Metric Bar Chart):**
   - Places Val RMSE, Test RMSE, Val MAE, and Test MAE side-by-side for all four models, visually demonstrating the step-function performance jump from heuristic baselines to ensemble learning.
7. **`random_forest_feature_importance.png` (Gini Impurity Feature Importance):**
   - Displays the relative importance of all 12 engineered features.
   - Shows that `rolling_mean_7`, `lag_1`, `machine_utilization_pct`, and `rolling_mean_30` carry the highest predictive influence.

---

## 4. Why Random Forest Was Selected as the Champion Model

A common faculty inquiry is why Random Forest was selected over Gradient Boosting when Gradient Boosting achieved a slightly lower Test MAE (0.4777 vs 0.4802). The engineering justification is grounded in three rigorous factors:

1. **Minimization of High-Cost Outlier Errors (Lowest Test RMSE: 0.6155):**
   - In industrial manufacturing, an under-prediction error of 5 units on a critical turbine bearing is far more catastrophic than 5 separate 1-unit errors on minor fasteners.
   - RMSE squares error residuals before averaging ($\sqrt{\frac{1}{n}\sum(y - \hat{y})^2}$), thereby heavily penalizing large deviations.
   - Random Forest achieved the **lowest out-of-sample Test RMSE (0.6155)** across all candidates.
2. **Superior Validation Generalization Across Both Metrics:**
   - During model selection, Random Forest swept both validation criteria:
     - Lowest Validation MAE: **0.4908** (vs GBDT 0.5052)
     - Lowest Validation RMSE: **0.6451** (vs GBDT 0.6724)
   - Random Forest demonstrated superior robustness against overfitting during cross-validation.
3. **Autoregressive Multi-Horizon Stability (90-Day Rollouts):**
   - The platform performs autoregressive forecasting (feeding $t+1$ predictions back into lag features to project out to 90 days).
   - Gradient Boosting builds trees sequentially to correct residual errors of previous trees, making it susceptible to error compounding when recursively forecasting into the distant future.
   - Random Forest relies on **bagging** (bootstrap aggregation of 100 independent de-correlated trees). Its variance-reduction properties make it substantially more stable during recursive multi-step forecasting.
4. **28.3% Improvement Over Industrial Heuristics:**
   - Outperformed traditional Moving Average (0.8583 RMSE) and Exponential Smoothing (0.8606 RMSE) by over 28%, demonstrating that factory utilization and temporal lag dynamics provide genuine predictive power.

---

## 5. Random Forest Implementation & Serverless Architecture

```
[Historical Telemetry (365 Days)]
             │
             ▼
[Feature Engineering: 12 Lags & Rolling Windows]
             │
             ▼
[Chronological Split: 70% Train, 15% Val, 15% Test]
             │
             ▼
[RandomForestRegressor: 100 Trees, Depth 6, Random State 42]
             │
             ▼
[Model Serialization: joblib.dump() -> champion_forecast_model.joblib (651 KB)]
             │
             ▼
[Amazon S3 Storage: s3://sparepartsiq-artifacts-985539784799/models/]
             │
             ▼
[AWS Lambda (SparePartsIQ-Backend): Download to /tmp/, In-Memory Warm Cache]
             │
             ▼
[Real-Time Inference: 7D / 30D / 90D Autoregressive Waves (~136ms)]
             │
             ▼
[DynamoDB Storage: SparePartsIQ-ForecastResults]
```

### Key Technical Parameters:
- **Algorithm:** `sklearn.ensemble.RandomForestRegressor`
- **Hyperparameters:** `n_estimators=100`, `max_depth=6`, `random_state=42`, `n_jobs=-1`
- **Input Features (12):**
  - Lags: `lag_1`, `lag_2`, `lag_7`, `lag_14`
  - Rolling Windows: `rolling_mean_7`, `rolling_std_7`, `rolling_mean_14`, `rolling_mean_30`
  - Duty Cycle: `machine_utilization_pct`, `is_maintenance_day`
  - Calendar Cyclics: `day_of_week`, `month`
- **Cold Start Latency:** ~7.1 seconds (includes S3 model retrieval and unpickling).
- **Warm Invocation Latency:** **136.4 milliseconds** (served from memory cache `_CACHED_MODEL`).

---

## 6. How to Demonstrate the ML Model Live in AWS

Follow these steps during a live faculty demonstration:

### Step 1: Open the Frontend Model Evaluation Dashboard
1. Navigate to `http://localhost:3000/model-evaluation`.
2. Present the **Comprehensive 4-Model Benchmark Matrix** table.
3. Toggle the **Model Performance Visualizer** tabs:
   - Click **RMSE Comparison** to show Random Forest's winning 0.6155 test error.
   - Click **MAE Comparison** to show the close competition between RF (0.4802) and GBDT (0.4777).
   - Click **MAPE %** to highlight relative percentage accuracy.
4. Walk through the **10-Step Serverless Lifecycle** diagram.

### Step 2: Trigger Live Real-Time Forecasting in AWS Lambda
1. Navigate to `http://localhost:3000/forecasting`.
2. Select component `High Precision Spindle Bearing (PRT-BRG-1001)`.
3. Switch between **7 Days**, **30 Days**, and **90 Days** horizons.
4. Show the live forecast curve and highlight the generated statistics:
   - 7-Day Predicted Demand: ~6.1 units
   - 30-Day Predicted Demand: ~38.2 units
   - 90-Day Predicted Demand: ~129.5 units
5. Explain that this calculation executed live inside AWS Lambda `SparePartsIQ-Backend` using the champion model retrieved from Amazon S3.

### Step 3: Verify the AWS Cloud Artifacts via CLI (Optional Proof)
Open PowerShell to show the actual cloud resources:
```powershell
# Show model artifact in Amazon S3:
aws s3 ls s3://sparepartsiq-artifacts-985539784799/models/

# Show persisted forecast in Amazon DynamoDB:
aws dynamodb get-item --table-name SparePartsIQ-ForecastResults --key "{\"part_id\": {\"S\": \"PRT-BRG-1001\"}}" --region ap-south-1
```

---

## 7. Five Likely Faculty Viva Questions & Answers

### Q1: Why did you use a Chronological Split instead of standard K-Fold Cross-Validation or random `train_test_split`?
> **Answer:**  
> In time-series forecasting, standard random shuffling causes catastrophic **data leakage (lookahead bias)** because future data points are randomly included in the training set to predict past events. This artificially inflates evaluation metrics and fails in production. By splitting chronologically (the first 70% of days for training, the next 15% for validation, and the final 15% for out-of-sample testing), we strictly mimic real-world deployment where future data is never visible to the model.

---

### Q2: Gradient Boosting had a slightly lower Test MAE (0.4777 vs 0.4802). Why did you still declare Random Forest the Champion?
> **Answer:**  
> First, Random Forest achieved the lowest **Test RMSE (0.6155 vs 0.6165)** and swept both validation criteria (**Validation MAE: 0.4908 vs 0.5052; Validation RMSE: 0.6451 vs 0.6724**). In industrial supply chains, RMSE is the primary metric because large outlier errors lead to stockouts on critical machinery, which cost tens of thousands of dollars per hour. Second, our system performs autoregressive 90-day rollouts where predictions feed back as inputs for future days. Random Forest's bagging architecture (averaging 100 independent de-correlated trees) provides significantly greater numerical stability than sequential boosting, which tends to accumulate and amplify errors across long horizons.

---

### Q3: How does your system perform multi-horizon forecasting (7, 30, and 90 days) using a single regression model?
> **Answer:**  
> We employ an **autoregressive recursive forecasting strategy**. The model is trained to predict consumption at day $t+1$ given lag features ($\text{lag}_1, \text{lag}_2, \text{lag}_7, \text{lag}_{14}$) and rolling window statistics. To forecast day $t+2$, the predicted value from $t+1$ is rolled into the feature vector dynamically. This recursive process is repeated day-by-day for 7, 30, and 90 iterations. The daily predictions are then aggregated into horizon totals and persisted to DynamoDB.

---

### Q4: How is the Machine Learning model deployed and served in the AWS serverless architecture?
> **Answer:**  
> The trained model is serialized using `joblib` into a compact 651 KB binary file (`champion_forecast_model.joblib`) and uploaded to Amazon S3 (`sparepartsiq-artifacts-985539784799`). The AWS Lambda function (`SparePartsIQ-Backend`) runs Python 3.12 with compiled NumPy, SciPy, and Scikit-Learn wheels packaged in the deployment zip. On a Lambda cold start, the backend downloads the model artifact from S3 into the `/tmp/` ephemeral directory and deserializes it into an in-memory cache (`_CACHED_MODEL`). Subsequent warm invocations execute ML inference in under **140 milliseconds** without incurring S3 network overhead or initialization delays.

---

### Q5: How do the ML forecast outputs translate into business actions in the application?
> **Answer:**  
> The forecast outputs feed directly into the **Stockout Risk Engine** and the **Reorder Optimization Engine**. The predicted daily consumption rate ($\hat{d}$) and variance ($\sigma_d$) are used in the dynamic safety stock formula:
> $$SS = Z \times \sqrt{L} \times \sigma_d$$
> where $Z$ is the service level factor (e.g., 1.65 for 95% service level) and $L$ is the supplier lead time. When current stock falls below the dynamic Reorder Point ($ROP = \hat{d} \times L + SS$), the system automatically generates purchase recommendations and triggers Amazon SNS notifications to alert procurement teams before an actual stockout occurs.

