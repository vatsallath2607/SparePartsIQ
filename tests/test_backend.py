import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_healthcheck():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["region"] == "ap-south-1"

def test_auth_login_success():
    response = client.post("/api/auth/login", json={
        "email": "inventory@sparepartsiq.com",
        "password": "Inventory@2026"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "inventory@sparepartsiq.com"
    assert data["user"]["role"] == "Inventory Manager"

def test_auth_login_invalid_password():
    response = client.post("/api/auth/login", json={
        "email": "inventory@sparepartsiq.com",
        "password": "WrongPassword!"
    })
    assert response.status_code == 401

@pytest.fixture
def auth_headers():
    res = client.post("/api/auth/login", json={
        "email": "inventory@sparepartsiq.com",
        "password": "Inventory@2026"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def purchase_auth_headers():
    res = client.post("/api/auth/login", json={
        "email": "purchase@sparepartsiq.com",
        "password": "Purchase@2026"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_inventory(auth_headers):
    response = client.get("/api/inventory", headers=auth_headers)
    assert response.status_code == 200
    parts = response.json()
    assert len(parts) >= 10
    first_part = parts[0]
    assert "part_id" in first_part
    assert "current_stock" in first_part
    assert "unit_cost" in first_part

def test_inventory_filters(auth_headers):
    response = client.get("/api/inventory?criticality=Critical", headers=auth_headers)
    assert response.status_code == 200
    parts = response.json()
    for p in parts:
        assert p["criticality_level"] == "Critical"

def test_get_low_stock(auth_headers):
    response = client.get("/api/inventory/low-stock", headers=auth_headers)
    assert response.status_code == 200
    parts = response.json()
    for p in parts:
        assert p["current_stock"] <= p["reorder_point"]

def test_forecast_endpoints(auth_headers):
    response = client.get("/api/forecasts", headers=auth_headers)
    assert response.status_code == 200
    forecasts = response.json()
    assert len(forecasts) > 0
    first_fc = forecasts[0]
    assert "forecast_horizons" in first_fc

def test_model_evaluation_metrics(auth_headers):
    response = client.get("/api/forecasts/evaluation/metrics", headers=auth_headers)
    assert response.status_code == 200
    metrics = response.json()
    assert "models_evaluated" in metrics
    assert "Random_Forest_Regressor" in metrics["models_evaluated"]
    assert "Moving_Average_7D" in metrics["models_evaluated"]

def test_stockout_risks(auth_headers):
    response = client.get("/api/stockouts", headers=auth_headers)
    assert response.status_code == 200
    risks = response.json()
    assert len(risks) > 0
    assert "risk_level" in risks[0]
    assert "risk_score" in risks[0]
    assert "risk_reason" in risks[0]

def test_maintenance_and_at_risk(auth_headers):
    res_machines = client.get("/api/maintenance/machines", headers=auth_headers)
    assert res_machines.status_code == 200
    assert len(res_machines.json()) >= 8
    
    res_schedules = client.get("/api/maintenance/schedules", headers=auth_headers)
    assert res_schedules.status_code == 200
    assert len(res_schedules.json()) >= 5
    
    res_at_risk = client.get("/api/maintenance/at-risk", headers=auth_headers)
    assert res_at_risk.status_code == 200
    assert isinstance(res_at_risk.json(), list)

def test_reorder_recommendations_and_decision(purchase_auth_headers):
    res = client.get("/api/reorders", headers=purchase_auth_headers)
    assert res.status_code == 200
    recs = res.json()
    assert len(recs) > 0
    first_rec = recs[0]
    rec_id = first_rec["recommendation_id"]
    
    # Test approval
    approve_res = client.post(
        f"/api/reorders/{rec_id}/approve",
        headers=purchase_auth_headers,
        json={"decision_notes": "Automated pytest approval verification"}
    )
    assert approve_res.status_code == 200
    appr_data = approve_res.json()
    assert appr_data["recommendation"]["status"] == "Approved"
    assert "purchase_order" in appr_data

def test_dashboard_analytics(auth_headers):
    response = client.get("/api/analytics/dashboard", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "kpis" in data
    assert data["kpis"]["total_spare_parts"] >= 10
    assert data["kpis"]["total_inventory_value"] > 0
    assert "category_distribution" in data
    assert "consumption_trend" in data
    assert "supplier_scorecard" in data

def test_notifications_and_alerts(auth_headers):
    res = client.get("/api/notifications", headers=auth_headers)
    assert res.status_code == 200
    notifs = res.json()
    assert len(notifs) >= 1
    
    # Test sending alert
    alert_payload = {
        "recipient_role": "Inventory Manager",
        "alert_type": "STOCKOUT_ALERT",
        "priority": "HIGH",
        "title": "Automated Pytest Inventory Notification",
        "message": "Routine automated CI/CD test alert verification."
    }
    alert_res = client.post("/api/notifications/alert", headers=auth_headers, json=alert_payload)
    assert alert_res.status_code == 200
    alert_data = alert_res.json()
    assert "notification" in alert_data
    assert alert_data["notification"]["title"] == alert_payload["title"]

