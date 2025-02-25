import pandas as pd
from pydantic import BaseModel
from catboost import CatBoostRegressor
from fastapi import APIRouter, HTTPException

MODEL_PATH = "./models/estimate_delivery_time/estimate_delivery_time.cb" #Catboost Model Path


# Define the route for Estimate Delivery Time prediction
router = APIRouter()


# Load the CatBoost regression model
try:
    model = CatBoostRegressor()
    model.load_model(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load Estimate Delivery Time model: {e}")


# Request schema for regression model
class EstimateDeliveryTimeModel(BaseModel):
    courier_partner: str
    to_state: str
    to_longitude: float
    to_latitude: float
    from_pincode: str
    distance_in_km: float


@router.post("/")
def EstimateDeliveryTime(request: EstimateDeliveryTimeModel):
    try:
        input_data = pd.DataFrame([request.model_dump()])

        # Define categorical columns for catboost
        categorical_columns = ["courier_partner", "to_state", "from_pincode"]
        input_data[categorical_columns] = input_data[categorical_columns].astype(str)

        # Get the predication
        prediction = model.predict(input_data)

        # Return the result
        return {"result": prediction[0]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not run Estimate Delivery Time : {e}")