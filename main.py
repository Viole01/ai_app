from fastapi import FastAPI
from models.address_quality_score.address_quality_score import router as address_quality_score_router
from models.estimate_delivery_time.estimate_delivery_time import router as estimate_delivery_time_router

# Instantiate app instance
app = FastAPI()

# For testing if application is running or not
@app.get("/")
def home():
    return {"message": "Welcome to the Healthmug AI Brain"}

# Include the routes for each model
app.include_router(address_quality_score_router, prefix="/address/quality-check")
app.include_router(estimate_delivery_time_router, prefix="/courier/estimate-delivery-time")
