from typing import List
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from model import load_model

app = FastAPI(
    title="Bank Note Authentication API",
    description="A simple API for verification of bank note",
    version="1.0.0",
)
model = load_model()

class PredictAuthenticationRequest(BaseModel):
    data: List[List[float]]

class PredictAuthenticationResponse(BaseModel):
    data: List[float]

@app.post("/predict", response_model=PredictAuthenticationResponse, tags=['prediction'])
async def predict(input: PredictAuthenticationRequest):
    X = np.array(input.data)
    y_pred = model.predict(X)
    result = PredictAuthenticationResponse(data=y_pred.tolist())
    return result

@app.get('/healthcheck', status_code=200, tags=['health_check'])
async def healthcheck():
    return 'Bank Note Authentication Classifier is ready!'