import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
from data_generator import generate_dataset
from preprocess import build_feature_dataframe
from model import build_autoencoder
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Generate data
transactions = generate_dataset()

# 2. Build per-merchant features
features_df = build_feature_dataframe(transactions)

# 3. Select features
feature_cols = [
    'peak_hour',
    'average_transactions_per_hour',
    'high_value_transaction_ratio',
    'late_night_frequency',
    'unique_customer_count',
    'time_diff_minutes'
]

X = features_df[feature_cols]

# 4. Split normal vs test (as per your logic)
split_ratio = 0.8
split_idx = int(len(X) * split_ratio)

normal_X = X.iloc[:split_idx]
test_X   = X.iloc[split_idx:]

# 5. Normalize
scaler = MinMaxScaler()
X_train = scaler.fit_transform(normal_X)
X_test = scaler.transform(test_X)

# 6. Train model
autoencoder = build_autoencoder(input_dim=X_train.shape[1])
autoencoder.fit(
    X_train, X_train,
    epochs=50,
    batch_size=32,
    shuffle=True,
    validation_split=0.2
)

# 7. Threshold
train_recon = autoencoder.predict(X_train)
train_errors = np.mean((X_train - train_recon) ** 2, axis=1)
threshold = np.percentile(train_errors, 95)

# 8. Save artifacts (IMPORTANT)
autoencoder.save(os.path.join(BASE_DIR, "autoencoder.keras"))
np.save(os.path.join(BASE_DIR, "threshold.npy"), threshold)
joblib.dump(scaler, os.path.join(BASE_DIR, "scaler.joblib"))



from rules import apply_rule_based_scoring

rule_scores = apply_rule_based_scoring(transactions)
print(rule_scores.head())

# print(features_df.columns.tolist())
features_df.to_csv("features_debug.csv", index=False)

