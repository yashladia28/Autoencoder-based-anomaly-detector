from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from anomaly_detector.infer import predict_anomaly


# ----------------------------
# FastAPI app
# ----------------------------
app = FastAPI(
    title="Merchant Anomaly Detection API",
    description="Unsupervised anomaly detection using an autoencoder",
    version="1.0"
)


# ----------------------------
# Input schema
# ----------------------------
class MerchantFeatures(BaseModel):
    peak_hour: float
    average_transactions_per_hour: float
    high_value_transaction_ratio: float
    late_night_frequency: float
    unique_customer_count: float
    time_diff_minutes: float

@app.get("/")
def root():
    return {
        "message": "Merchant Anomaly Detection API is running",
        "docs": "/docs"
    }

# ----------------------------
# Prediction endpoint
# ----------------------------
@app.post("/predict")
def predict(features: MerchantFeatures):
    try:
        feature_vector = [
            features.peak_hour,
            features.average_transactions_per_hour,
            features.high_value_transaction_ratio,
            features.late_night_frequency,
            features.unique_customer_count,
            features.time_diff_minutes
        ]

        result = predict_anomaly(feature_vector)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
