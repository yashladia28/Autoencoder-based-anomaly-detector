Merchant Transaction Anomaly Detection System

This repository contains an end-to-end unsupervised learning pipeline designed to identify suspicious merchant behavior. The system utilizes a Deep Learning Autoencoder architecture combined with rule-based heuristics to flag transactions that deviate from established historical patterns.
Project Overview

The system detects anomalies by learning the latent representation of "normal" merchant activity. By measuring the reconstruction error of incoming data, the model can effectively flag outliers that do not conform to learned behaviors.

Key Components:

    Synthetic Data Engine: Generates realistic merchant transaction logs.

    Feature Engineering: Aggregates raw transaction data into merchant-level behavioral vectors.

    Unsupervised Learning: Autoencoder model trained on non-anomalous samples.

    Inference Service: A production-ready FastAPI implementation for real-time scoring.

System Architecture

The pipeline is structured to ensure a clean separation between data processing, model state, and the serving layer:

    Ingestion: Raw transaction logs are processed.

    Engineering: Features such as peak hours and customer density are calculated per merchant.

    Normalization: Data is transformed via a fitted MinMaxScaler.

    Reconstruction: The Autoencoder attempts to reconstruct the input vector.

    Decision Logic: Anomaly status is determined by comparing the Mean Squared Error (MSE) against a predefined 95th percentile threshold.

Project Structure
Plaintext

## Project Structure
```
anomaly_detector/

├── app.py                 # FastAPI application entry point
├── data_generator.py      # Script for generating synthetic transaction datasets
├── preprocess.py          # Data cleaning and feature engineering logic
├── train.py               # Training pipeline for the Autoencoder
├── infer.py               # Core inference and scoring logic
├── rules.py               # Deterministic rule-based scoring components
├── autoencoder.keras      # Serialized model weights
├── scaler.joblib          # Persisted MinMaxScaler state
└── threshold.npy          # Calculated anomaly threshold value
```

Feature Engineering

The model analyzes merchant behavior through several high-signal features:

    Temporal Patterns: Peak transaction hours and frequency of late-night activity.

    Volume Metrics: Average transactions per hour and unique customer counts.

    Risk Indicators: Ratio of high-value transactions and time delta between consecutive events.

Technical Implementation
Autoencoder Specifications

    Type: Fully connected (Dense) Neural Network.

    Loss Function: Mean Squared Error (MSE).

    Optimization: Trained exclusively on "normal" behavior to ensure high reconstruction error on anomalous data.

    Thresholding: The decision boundary is set at the 95th percentile of training reconstruction errors.

API Deployment

The system is served via FastAPI. To initialize the service locally:
Bash

uvicorn anomaly_detector.app:app --reload

The interactive API documentation is available at http://127.0.0.1:8000/docs.
API Reference
Predict Anomaly

Endpoint: POST /predict

Request Body:
JSON

{
  "peak_hour": 12,
  "average_transactions_per_hour": 30.0,
  "high_value_transaction_ratio": 0.0,
  "late_night_frequency": 0.0,
  "unique_customer_count": 30,
  "time_diff_minutes": 1440.0
}

Response:
JSON

{
  "anomaly_score": 0.0003,
  "threshold": 0.00049,
  "is_anomalous": false
}

Technology Stack

    Core: Python

    Deep Learning: TensorFlow / Keras

    Data Science: Scikit-learn, NumPy, Pandas

    Web Framework: FastAPI

    Utilities: Joblib (Serialization), Faker (Data Generation)

Future Roadmap

    Implementation of batch inference for asynchronous processing.

    Integration with persistent databases (PostgreSQL/MongoDB) for real-time ingestion.

    Drift monitoring for anomaly scores to detect evolving fraud patterns.

    Containerization via Docker for cloud-native deployment.

Author: Yash Ladia


Engineering student focused on Machine Learning, Computer Vision, and Scalable ML Systems.



