from fastapi import APIRouter, Depends
import json
import os
from backend.auth import get_current_user

router = APIRouter(prefix="/api/stockouts", tags=["Stockout Risk Prediction"])

def _get_stockout_path() -> str:
    if os.path.exists("data/stockout_risks.json"):
        return "data/stockout_risks.json"
    pkg_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "stockout_risks.json")
    if os.path.exists(pkg_path):
        return pkg_path
    lambda_path = os.path.join("/var/task", "data", "stockout_risks.json")
    if os.path.exists(lambda_path):
        return lambda_path
    return "data/stockout_risks.json"

@router.get("")
def get_stockout_risks(user: dict = Depends(get_current_user)):
    file_path = _get_stockout_path()
    if os.path.exists(file_path):
        with open(file_path) as f:
            risks = json.load(f)
            # Sort by risk severity: Critical, High, Medium, Low
            severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
            risks.sort(key=lambda x: (severity_order.get(x.get("risk_level", "Low"), 4), -x.get("risk_score", 0)))
            return risks
    return []

@router.get("/summary")
def get_stockout_summary(user: dict = Depends(get_current_user)):
    file_path = _get_stockout_path()
    summary = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "TotalAssessed": 0}
    if os.path.exists(file_path):
        with open(file_path) as f:
            risks = json.load(f)
            summary["TotalAssessed"] = len(risks)
            for r in risks:
                lvl = r.get("risk_level", "Low")
                if lvl in summary:
                    summary[lvl] += 1
    return summary

