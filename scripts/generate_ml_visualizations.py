"""
Generate professional, presentation-ready ML benchmark graphs for faculty evaluation.
Strictly verified against ml/artifacts/evaluation_report.json.
"""
import os
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = r"C:\Users\Public\SparePartsIQ\docs\ml_visualizations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

REPORT_PATH = r"C:\Users\Public\SparePartsIQ\ml\artifacts\evaluation_report.json"
with open(REPORT_PATH, "r") as f:
    report = json.load(f)

models_data = report["models_evaluated"]

# Model labels for presentation
model_keys = [
    "Moving_Average_7D",
    "Exponential_Smoothing",
    "Gradient_Boosting_Regressor",
    "Random_Forest_Regressor"
]

model_labels = [
    "Simple Moving Avg (7D)",
    "Exponential Smoothing (α=0.3)",
    "Gradient Boosting Regressor",
    "Random Forest Regressor (Champion)"
]

# Style settings
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
colors = ['#94a3b8', '#94a3b8', '#38bdf8', '#10b981']  # Gray for baselines, blue for GBDT, green for RF champion

# 1. Validation RMSE Comparison
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
val_rmse = [models_data[k]["validation"]["RMSE"] for k in model_keys]
bars = ax.bar(model_labels, val_rmse, color=colors, width=0.55, edgecolor='#1e293b', linewidth=1.2)
ax.set_ylabel("Validation RMSE (Lower is Better)", fontsize=11, fontweight='bold', labelpad=10)
ax.set_title("Validation Root Mean Squared Error (RMSE) Comparison\nEvaluated on Out-of-Sample Validation Split (15%)", fontsize=13, fontweight='bold', pad=15)
ax.set_ylim(0, max(val_rmse) * 1.25)
ax.axhline(val_rmse[3], color='#10b981', linestyle='--', alpha=0.7, label=f'Champion Threshold ({val_rmse[3]:.4f})')

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.4f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.legend(loc='upper right', frameon=True)
plt.xticks(rotation=12, ha='right', fontsize=9, fontweight='medium')
plt.tight_layout()
p1 = os.path.join(OUTPUT_DIR, "val_rmse_comparison.png")
plt.savefig(p1)
plt.close()
print("Generated:", p1)

# 2. Test RMSE Comparison
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
test_rmse = [models_data[k]["test"]["RMSE"] for k in model_keys]
bars = ax.bar(model_labels, test_rmse, color=colors, width=0.55, edgecolor='#1e293b', linewidth=1.2)
ax.set_ylabel("Test RMSE (Lower is Better)", fontsize=11, fontweight='bold', labelpad=10)
ax.set_title("Test Root Mean Squared Error (RMSE) Comparison\nEvaluated on Chronological Out-of-Sample Test Split (15%)", fontsize=13, fontweight='bold', pad=15)
ax.set_ylim(0, max(test_rmse) * 1.25)
ax.axhline(test_rmse[3], color='#10b981', linestyle='--', alpha=0.7, label=f'Champion Lowest RMSE ({test_rmse[3]:.4f})')

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.4f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.legend(loc='upper right', frameon=True)
plt.xticks(rotation=12, ha='right', fontsize=9, fontweight='medium')
plt.tight_layout()
p2 = os.path.join(OUTPUT_DIR, "test_rmse_comparison.png")
plt.savefig(p2)
plt.close()
print("Generated:", p2)

# 3. Validation MAE Comparison
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
val_mae = [models_data[k]["validation"]["MAE"] for k in model_keys]
bars = ax.bar(model_labels, val_mae, color=colors, width=0.55, edgecolor='#1e293b', linewidth=1.2)
ax.set_ylabel("Validation MAE (Lower is Better)", fontsize=11, fontweight='bold', labelpad=10)
ax.set_title("Validation Mean Absolute Error (MAE) Comparison\nAverage Daily Consumption Prediction Error", fontsize=13, fontweight='bold', pad=15)
ax.set_ylim(0, max(val_mae) * 1.25)
ax.axhline(val_mae[3], color='#10b981', linestyle='--', alpha=0.7, label=f'Champion Lowest Val MAE ({val_mae[3]:.4f})')

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.4f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.legend(loc='upper right', frameon=True)
plt.xticks(rotation=12, ha='right', fontsize=9, fontweight='medium')
plt.tight_layout()
p3 = os.path.join(OUTPUT_DIR, "val_mae_comparison.png")
plt.savefig(p3)
plt.close()
print("Generated:", p3)

# 4. Test MAE Comparison
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
test_mae = [models_data[k]["test"]["MAE"] for k in model_keys]
bars = ax.bar(model_labels, test_mae, color=colors, width=0.55, edgecolor='#1e293b', linewidth=1.2)
ax.set_ylabel("Test MAE (Lower is Better)", fontsize=11, fontweight='bold', labelpad=10)
ax.set_title("Test Mean Absolute Error (MAE) Comparison\nOut-of-Sample Generalization Across 64 Industrial Components", fontsize=13, fontweight='bold', pad=15)
ax.set_ylim(0, max(test_mae) * 1.25)
ax.axhline(test_mae[2], color='#38bdf8', linestyle=':', alpha=0.8, label=f'GBDT Test MAE ({test_mae[2]:.4f})')
ax.axhline(test_mae[3], color='#10b981', linestyle='--', alpha=0.8, label=f'RF Test MAE ({test_mae[3]:.4f})')

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.4f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.legend(loc='upper right', frameon=True)
plt.xticks(rotation=12, ha='right', fontsize=9, fontweight='medium')
plt.tight_layout()
p4 = os.path.join(OUTPUT_DIR, "test_mae_comparison.png")
plt.savefig(p4)
plt.close()
print("Generated:", p4)

# 5. MAPE Comparison
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
test_mape = [models_data[k]["test"]["MAPE_pct"] for k in model_keys]
bars = ax.bar(model_labels, test_mape, color=colors, width=0.55, edgecolor='#1e293b', linewidth=1.2)
ax.set_ylabel("Test MAPE % (Lower is Better)", fontsize=11, fontweight='bold', labelpad=10)
ax.set_title("Mean Absolute Percentage Error (MAPE %) Comparison\nRelative Error on Non-Zero Daily Spare Parts Consumption", fontsize=13, fontweight='bold', pad=15)
ax.set_ylim(0, max(test_mape) * 1.25)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f"{yval:.2f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.xticks(rotation=12, ha='right', fontsize=9, fontweight='medium')
plt.tight_layout()
p5 = os.path.join(OUTPUT_DIR, "test_mape_comparison.png")
plt.savefig(p5)
plt.close()
print("Generated:", p5)

# 6. Overall Multi-Metric Consolidated Comparison Matrix
fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
x = np.arange(len(model_labels))
width = 0.22

rects1 = ax.bar(x - 1.5*width, val_rmse, width, label='Val RMSE', color='#60a5fa')
rects2 = ax.bar(x - 0.5*width, test_rmse, width, label='Test RMSE', color='#0284c7')
rects3 = ax.bar(x + 0.5*width, val_mae, width, label='Val MAE', color='#a7f3d0')
rects4 = ax.bar(x + 1.5*width, test_mae, width, label='Test MAE', color='#059669')

ax.set_ylabel('Error Score (Lower is Better)', fontsize=11, fontweight='bold')
ax.set_title('Comprehensive Out-of-Sample Error Metric Comparison Across All 4 Evaluated Models', fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(model_labels, fontsize=9, fontweight='medium', rotation=10, ha='right')
ax.legend(loc='upper right', frameon=True, fontsize=10)
ax.set_ylim(0, 1.1)

# Annotate values
for rects in [rects1, rects2, rects3, rects4]:
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f'{h:.2f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=7, fontweight='bold')

plt.tight_layout()
p6 = os.path.join(OUTPUT_DIR, "overall_model_benchmark_matrix.png")
plt.savefig(p6)
plt.close()
print("Generated:", p6)

# 7. Random Forest Feature Importances
model_path = r"C:\Users\Public\SparePartsIQ\ml\artifacts\champion_forecast_model.joblib"
if os.path.exists(model_path):
    rf_model = joblib.load(model_path)
    importances = rf_model.feature_importances_
    features = report["features"]
    
    # Sort features by importance
    idx = np.argsort(importances)
    sorted_features = [features[i] for i in idx]
    sorted_importances = importances[idx]
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    y_pos = np.arange(len(sorted_features))
    bars = ax.barh(y_pos, sorted_importances, color='#10b981', edgecolor='#065f46', height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_features, fontsize=10, fontweight='medium')
    ax.set_xlabel('Gini Impurity Feature Importance (Normalized)', fontsize=11, fontweight='bold')
    ax.set_title('Random Forest Champion Model: Feature Importance Distribution\nEngineered Across 12 Lags, Rolling Windows & Equipment Telemetry Features', fontsize=12, fontweight='bold', pad=15)
    
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.005, bar.get_y() + bar.get_height()/2.0, f'{w*100:.1f}%', va='center', fontsize=9, fontweight='bold')
        
    ax.set_xlim(0, max(sorted_importances) * 1.2)
    plt.tight_layout()
    p7 = os.path.join(OUTPUT_DIR, "random_forest_feature_importance.png")
    plt.savefig(p7)
    plt.close()
    print("Generated:", p7)

print("All ML visualization graphs successfully created in docs/ml_visualizations/")

