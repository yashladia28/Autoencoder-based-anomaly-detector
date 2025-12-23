import pandas as pd
import numpy as np

# Sample DataFrame with necessary columns
df = pd.DataFrame(transactions)

# 4.1 High Velocity Detection (Transactions per hour threshold)

# Group by 'merchant_id' and calculate the transaction frequency (velocity) per hour
df['hour'] = df['timestamp'].dt.hour
transaction_counts = df.groupby(['merchant_id', 'hour']).size().reset_index(name='transaction_count')

# Define a threshold for high velocity (e.g., more than 3 transactions per hour considered high velocity)
high_velocity_threshold = 3
high_velocity = transaction_counts[transaction_counts['transaction_count'] > high_velocity_threshold]

print("High Velocity Transactions:")
print(high_velocity)

# 4.2 Odd-Hour Pattern Detection (Transactions outside business hours)
# Let's assume normal business hours are 9 AM to 6 PM (odd hours are outside this range)

business_hours_start = 9
business_hours_end = 18

# Mark transactions occurring outside business hours as 'odd hour'
df['is_odd_hour'] = df['hour'].apply(lambda x: x < business_hours_start or x > business_hours_end)

print("\nOdd-Hour Pattern Detection:")
print(df[df['is_odd_hour'] == True])

# 4.3 Customer Concentration Analysis
# If a merchant has a high number of transactions from the same customer, it could indicate concentration risk.

# Count transactions per customer for each merchant
customer_concentration = df.groupby(['merchant_id', 'customer_id']).size().reset_index(name='customer_transaction_count')

# Define a threshold for high concentration (e.g., more than 3 transactions per customer considered high concentration)
high_concentration_threshold = 2
high_concentration = customer_concentration[customer_concentration['customer_transaction_count'] >= high_concentration_threshold]

print("\nCustomer Concentration Analysis:")
print(high_concentration)

# 4.4 Calculate Pattern-Specific Scores
# Example scoring based on the above patterns (high velocity, odd-hour, and customer concentration)

df['high_velocity_score'] = df['merchant_id'].map(lambda x: 1 if x in high_velocity['merchant_id'].values else 0)
df['odd_hour_score'] = df['is_odd_hour'].astype(int)  # 1 if in odd hours, 0 otherwise
df['customer_concentration_score'] = df['merchant_id'].map(lambda x: 1 if x in high_concentration['merchant_id'].values else 0)

# Calculate final anomaly score based on these rules
df['total_anomaly_score'] = df['high_velocity_score'] + df['odd_hour_score'] + df['customer_concentration_score']

print("\nPattern-Specific Scores:")
print(df[['merchant_id', 'transaction_id', 'high_velocity_score', 'odd_hour_score', 
          'customer_concentration_score', 'total_anomaly_score']])