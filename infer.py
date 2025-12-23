import numpy as np
from keras.models import load_model
import joblib
import os

# ----------------------------
# Load trained artifacts
# ----------------------------
def load_artifacts(
    model_path="autoencoder.keras",
    threshold_path="threshold.npy",
    scaler_path="scaler.joblib"
):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    model = load_model(os.path.join(base_dir, model_path))
    threshold = np.load(os.path.join(base_dir, threshold_path))
    scaler = joblib.load(os.path.join(base_dir, scaler_path))

    return model, threshold, scaler


# ----------------------------
# Normalize input features
# ----------------------------


# ----------------------------
# Inference function
# ----------------------------
def predict_anomaly(feature_vector):
    """
    feature_vector: list or numpy array of shape (n_features,)
    returns: anomaly score and decision
    """

    model, threshold, scaler = load_artifacts()


    # Convert input to numpy array
    feature_vector = np.array(feature_vector).reshape(1, -1)

    # Normalize
    scaled_features = scaler.transform(feature_vector)


    # Reconstruct
    reconstructed = model.predict(scaled_features, verbose=0)

    # Compute reconstruction error
    reconstruction_error = np.mean(
        np.square(scaled_features - reconstructed), axis=1
    )[0]

    # Anomaly decision
    is_anomalous = reconstruction_error > threshold

    return {
        "anomaly_score": float(reconstruction_error),
        "threshold": float(threshold),
        "is_anomalous": bool(is_anomalous)
    }



# if __name__ == "__main__":
#     sample_features = [
#         1.0,    # peak_hour
#         0.8,    # average_transactions_per_hour
#         0.2,    # high_value_transaction_ratio
#         0.1,    # late_night_frequency
#         50,     # unique_customer_count
#         12.3    # time_diff_minutes
#     ]

#     result = predict_anomaly(sample_features)
#     print(result)
