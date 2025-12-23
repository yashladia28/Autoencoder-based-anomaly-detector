import pandas as pd
from collections import defaultdict, Counter
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def transactions_to_df(transactions):
    df = pd.DataFrame(transactions)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    return df

def average_transactions_per_hour(df):
    hourly = (
        df.groupby(["merchant_id", "hour"])
        .size()
        .reset_index(name="transaction_count")
    )
    return (
        hourly.groupby("merchant_id")["transaction_count"]
        .mean()
        .reset_index(name="average_transactions_per_hour")
    )

def transaction_time_diff(df):
    df = df.sort_values(["merchant_id", "timestamp"])
    df["time_diff_minutes"] = (
        df.groupby("merchant_id")["timestamp"]
        .diff()
        .dt.total_seconds() / 60
    )
    return df[["merchant_id", "time_diff_minutes"]]

def avg_time_between_transactions(df):
    df = df.sort_values(["merchant_id", "timestamp"])
    df["time_diff_minutes"] = (
        df.groupby("merchant_id")["timestamp"]
        .diff()
        .dt.total_seconds() / 60
    )

    return (
        df.groupby("merchant_id")["time_diff_minutes"]
        .mean()
        .reset_index(name="time_diff_minutes")
    )


def peak_transaction_hour(transactions):
    merchant_hours = defaultdict(list)
    for txn in transactions:
        merchant_hours[txn["merchant_id"]].append(txn["timestamp"].hour)

    rows = []
    for m, hours in merchant_hours.items():
        peak = Counter(hours).most_common(1)[0][0]
        rows.append({"merchant_id": m, "peak_hour": peak})

    return pd.DataFrame(rows)

def late_night_frequency(transactions):
    LATE_HOURS = set(range(23, 24)) | set(range(0, 5))
    stats = defaultdict(lambda: {"total": 0, "late": 0})

    for txn in transactions:
        m = txn["merchant_id"]
        stats[m]["total"] += 1
        if txn["timestamp"].hour in LATE_HOURS:
            stats[m]["late"] += 1

    return pd.DataFrame([
        {
            "merchant_id": m,
            "late_night_frequency": v["late"] / v["total"]
        }
        for m, v in stats.items()
    ])

def amount_statistics(df):
    return df.groupby("merchant_id")["amount"].agg(
        average_transaction_amount="mean",
        variance_transaction_amount="var"
    ).reset_index()

def unique_customer_count(df):
    return (
        df.groupby("merchant_id")["customer_id"]
        .nunique()
        .reset_index(name="unique_customer_count")
    )

def high_value_transaction_ratio(df, threshold=10000):
    df = df.copy()
    df["is_high_value"] = df["amount"] > threshold

    return (
        df.groupby("merchant_id")["is_high_value"]
        .mean()
        .reset_index(name="high_value_transaction_ratio")
    )


#Orchestration function
def build_feature_dataframe(transactions):
    df = transactions_to_df(transactions)

    features = (
        df[["merchant_id"]]
        .drop_duplicates()
        .merge(average_transactions_per_hour(df), on="merchant_id")
        .merge(peak_transaction_hour(transactions), on="merchant_id")
        .merge(late_night_frequency(transactions), on="merchant_id")
        .merge(amount_statistics(df), on="merchant_id")
        .merge(unique_customer_count(df), on="merchant_id")
        .merge(high_value_transaction_ratio(df), on="merchant_id")   # ✅ ADD
        .merge(avg_time_between_transactions(df), on="merchant_id")  # ✅ ADD
    )

    return features


def build_scaler(feature_columns):
    return MinMaxScaler(), feature_columns

