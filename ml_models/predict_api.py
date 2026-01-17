from pathlib import Path
from typing import Optional
import uvicorn

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent
DURATION_MODEL_PATH = ROOT / "duration_model.pkl"
BUDGET_MODEL_PATH = ROOT / "budget_model.pkl"


def _load_model(path: Path):
    if not path.exists():
        return None
    return joblib.load(path)


duration_model = _load_model(DURATION_MODEL_PATH)
budget_model = _load_model(BUDGET_MODEL_PATH)

app = FastAPI(title="Prediction API", version="0.1")


class DurationRequest(BaseModel):
    city: str
    interest: str
    attractions: int


class DurationResponse(BaseModel):
    predicted_duration: str


class BudgetRequest(BaseModel):
    city: str
    days: int
    travel_type: str
    interest: str


class BudgetResponse(BaseModel):
    predicted_budget: float


@app.get("/health")
def health():
    return {
        "status": "ok",
        "duration_model_loaded": duration_model is not None,
        "budget_model_loaded": budget_model is not None,
    }


@app.post("/predict/duration", response_model=DurationResponse)
def predict_duration(req: DurationRequest):
    if duration_model is None:
        raise HTTPException(status_code=503, detail="Duration model not loaded")

    df = pd.DataFrame([req.dict()])
    try:
        pred = duration_model.predict(df)
        return {"predicted_duration": str(pred[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/budget", response_model=BudgetResponse)
def predict_budget(req: BudgetRequest):
    if budget_model is None:
        raise HTTPException(status_code=503, detail="Budget model not loaded")

    df = pd.DataFrame([req.dict()])
    try:
        pred = budget_model.predict(df)
        # ensure a float
        return {"predicted_budget": float(pred[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)