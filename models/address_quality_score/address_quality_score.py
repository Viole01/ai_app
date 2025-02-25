import fasttext
import pandas as pd
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from .address_quality_score_preprocess import process_and_predict

MODEL_PATH = "./models/address_quality_score/address_quality_score.bin" # Fasttext Model Path


# Define the route
router = APIRouter()


# Load the FastText text model
try:
    model = fasttext.load_model(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load Address Quality model: {e}")


# Request schema for text classification model
class AddressQualityScore(BaseModel):
    address: str
    address_line1: str
    landmark: str
    city: str
    state: str


@router.post("/")
def AddressQuality(request: AddressQualityScore):

    # Prepare the request data as a DataFrame
    input_data = pd.DataFrame([request.model_dump()])

    # Call the process_and_predict function to preprocess and predict
    result = process_and_predict(input_data, model_path=MODEL_PATH)

    # Convert the entire result DataFrame to a dictionary
    result_dict = result.to_dict(orient="records")

    # Return the result
    return {"result": {"predicted_quality": result_dict[0]["predicted_quality"], "probability": result_dict[0]["probability"]}}
    #return {"result": result_dict[0]} # For debugging and checking the complete results with input data
    
    # try:
    #     # Prepare the request data as a DataFrame
    #     input_data = pd.DataFrame([request.model_dump()])

    #     # Call the process_and_predict function to preprocess and predict
    #     result = process_and_predict(input_data, model_path=MODEL_PATH)

    #     # Convert the entire result DataFrame to a dictionary
    #     result_dict = result.to_dict(orient="records")

    #     # Return the result
    #     return {"result": {"predicted_quality": result_dict[0]["predicted_quality"], "probability": result_dict[0]["probability"]}}
    #     #return {"result": result_dict[0]} # For debugging and checking the complete results with input data
    
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Could not run Address Quality Check : {e}")