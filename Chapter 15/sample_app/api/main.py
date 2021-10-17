from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel, validator

from .ml.model import predict, preprocess, min_length


class PredictRequest(BaseModel):
    data: str

    @validator("data")
    def check_length(cls, t):
        if len(t) < min_length:
            raise ValueError(f"Text is too short! require at least {min_length} characters")
        return t

class PredictResponse(BaseModel):
    data: dict

app = FastAPI()

@app.get("/")
def health():
    return {"message": "API is working"}

@app.post("/predict", response_model=PredictResponse)
def predict_gender_content(input: PredictRequest):
    text = input.data
    resp = predict(text)
    result = PredictResponse(data=resp)
    return result