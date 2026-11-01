import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from backend.routers import (
    auth_routes,
    inventory_routes,
    forecast_routes,
    stockout_routes,
    reorder_routes,
    maintenance_routes,
    suppliers_routes,
    purchase_orders_routes,
    analytics_routes,
    notifications_routes,
)

app = FastAPI(
    title="SparePartsIQ API",
    description="Autonomous Industrial Spare Parts Intelligence & Inventory Optimization Platform API",
    version="1.0.0"
)

# Enterprise Scoped CORS configuration
# Explicit origins prevent arbitrary domain origin reflection while allowing credentials
configured_origins = os.getenv("ALLOWED_ORIGINS", "")
origins_list = [o.strip() for o in configured_origins.split(",") if o.strip()]
if not origins_list:
    origins_list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
)

# Register routers
app.include_router(auth_routes.router)
app.include_router(inventory_routes.router)
app.include_router(forecast_routes.router)
app.include_router(stockout_routes.router)
app.include_router(reorder_routes.router)
app.include_router(maintenance_routes.router)
app.include_router(suppliers_routes.router)
app.include_router(purchase_orders_routes.router)
app.include_router(analytics_routes.router)
app.include_router(notifications_routes.router)

@app.get("/health")
@app.get("/api/health")
def healthcheck():
    from backend.config import STORAGE_MODE, AWS_REGION
    return {
        "status": "HEALTHY",
        "service": "SparePartsIQ-Backend",
        "mode": STORAGE_MODE,
        "region": AWS_REGION,
        "version": "1.0.0"
    }

# AWS Lambda Handler Entrypoint
mangum_handler = Mangum(app)

def handler(event, context):
    # Detect EventBridge / CloudWatch Scheduled Event
    if isinstance(event, dict) and (event.get("source") == "aws.events" or event.get("detail-type") == "Scheduled Event"):
        import logging
        logger = logging.getLogger("SparePartsIQ.ScheduledEvent")
        logger.info("[EventBridge] Daily scheduled forecasting triggered by rule SparePartsIQ-DailyForecastingRule.")
        try:
            from backend.routers.forecast_routes import generate_and_save_forecast
            from backend.config import TABLE_PARTS
            from backend.db import dynamodb, decimal_to_native

            parts_table = dynamodb.Table(TABLE_PARTS)
            parts = decimal_to_native(parts_table.scan().get("Items", []))
            saved = []
            for part in parts[:5]:  # Run automated forecast for key components
                pid = part.get("part_id")
                if pid:
                    generate_and_save_forecast(pid)
                    saved.append(pid)
            logger.info(f"[EventBridge] Successfully persisted automated ML forecasts for {len(saved)} parts: {saved}")
            return {"status": "SUCCESS", "message": f"Daily forecasting completed for {len(saved)} parts", "parts": saved}
        except Exception as e:
            logger.error(f"[EventBridge] Scheduled forecasting failed: {e}")
            return {"status": "ERROR", "error": str(e)}

    return mangum_handler(event, context)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

