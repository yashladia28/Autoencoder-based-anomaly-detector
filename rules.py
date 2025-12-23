import pandas as pd

def apply_rule_based_scoring(transactions):
    df = pd.DataFrame(transactions)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour

    # 1. High velocity detection
    txn_counts = (
        df.groupby(["merchant_id", "hour"])
        .size()
        .reset_index(name="transaction_count")
    )

    high_velocity_merchants = set(
        txn_counts[txn_counts["transaction_count"] > 3]["merchant_id"]
    )

    # 2. Odd-hour detection
    business_start, business_end = 9, 18
    df["odd_hour_score"] = df["hour"].apply(
        lambda x: 1 if x < business_start or x > business_end else 0
    )

    # 3. Customer concentration
    cust_counts = (
        df.groupby(["merchant_id", "customer_id"])
        .size()
        .reset_index(name="count")
    )

    high_concentration_merchants = set(
        cust_counts[cust_counts["count"] >= 2]["merchant_id"]
    )

    # 4. Aggregate rule scores
    df["high_velocity_score"] = df["merchant_id"].apply(
        lambda x: 1 if x in high_velocity_merchants else 0
    )
    df["customer_concentration_score"] = df["merchant_id"].apply(
        lambda x: 1 if x in high_concentration_merchants else 0
    )

    df["rule_anomaly_score"] = (
        df["high_velocity_score"]
        + df["odd_hour_score"]
        + df["customer_concentration_score"]
    )

    return df[
        [
            "merchant_id",
            "transaction_id",
            "rule_anomaly_score",
            "high_velocity_score",
            "odd_hour_score",
            "customer_concentration_score",
        ]
    ]
