#Merchant data generation
import random
from faker import Faker
from datetime import datetime, timedelta

faker = Faker()

def generate_merchant_profiles(count):       # generate_merchant_base
    """Generate simplified merchant profiles."""
    merchants = []
    for _ in range(count):
        merchant = {
            "merchant_id": f"M{random.randint(1000, 9999)}",
            "business_name": faker.company(),
            "business_type": random.choice(["Retail", "E-commerce"]),
            "registration_date": faker.date_this_decade(),
            "average_ticket_size": round(random.uniform(1000, 10000), 2),
            # Registration Details
            "gst_status": random.choice([True, False]),         # GST registration status
        }
        merchants.append(merchant)
    return merchants


#Transactions Generation
#Creates and outputs transaction data for transactions held within the last 30 days assuming one transaction happens per day
#Function to generate normal transactions
def generate_normal_transactions(merchant_id,  amount_range):
    """Generate normal transaction patterns."""
    transactions = []
    num_days = 30
    for _ in range(num_days):
        txn = {
            "transaction_id": f"T{random.randint(100000, 999999)}",
            "merchant_id": merchant_id,
            "customer_id": f"C{random.randint(1000, 9999)}",
            "timestamp": datetime.now().replace(microsecond=0) - timedelta(days=random.randint(0, num_days)),
            "amount": round(random.uniform(*amount_range), 2),
            "status": "completed",
            "is_anomalous": False
        }
        transactions.append(txn)
    return transactions

#Function to generate anomalous transactions 
def generate_anomalous_transactions(merchant_id, pattern):
    """Generate anomalous transaction patterns based on a given fraud type."""
    transactions = []
    num_days = 30
    Constcustomer_id = f"C{random.randint(1000, 9999)}"  # Random customer ID
    for _ in range(num_days):
        
        # For customer concentration, we generate multiple transactions for the same customer
        if pattern == "customer_concentration":
            customer_id = Constcustomer_id  # Constant customer ID


            txn_time = datetime.now().replace(microsecond=0)
            amount = round(random.uniform(3000, 15000), 2)
            
            txn = {
                "transaction_id": f"T{random.randint(100000, 999999)}",
                "merchant_id": merchant_id,
                "customer_id": customer_id,  # Same customer repeats
                "timestamp": txn_time,
                "amount": amount,
                "status": "completed",
                "is_anomalous": True,
                "pattern": pattern
            }
            transactions.append(txn)

        # Handle other patterns (e.g., late_night, high_velocity) separately
        elif pattern == "late_night":
            
            hour = random.choice(list(range(23, 24)) + list(range(0, 5)))
            txn_time = datetime.now().replace(hour=hour, minute=random.randint(0, 59), second=0, microsecond=0)
            amount = round(random.uniform(5000, 20000), 2)
            
            txn = {
                "transaction_id": f"T{random.randint(100000, 999999)}",
                "merchant_id": merchant_id,
                "customer_id": f"C{random.randint(1000, 9999)}",  # Different customer ID
                "timestamp": txn_time,
                "amount": amount,
                "status": "completed",
                "is_anomalous": True,
                "pattern": pattern
            }
            transactions.append(txn)

        elif pattern == "high_velocity":
            txn_time = datetime.now().replace(microsecond=0)
            amount = round(random.uniform(2000, 10000), 2)
            
            txn = {
                "transaction_id": f"T{random.randint(100000, 999999)}",
                "merchant_id": merchant_id,
                "customer_id": f"C{random.randint(1000, 9999)}",  # Different customer ID
                "timestamp": txn_time,
                "amount": amount,
                "status": "completed",
                "is_anomalous": True,
                "pattern": pattern
            }
            transactions.append(txn)

        else:
        # Default case for any other patterns
            txn_time = datetime.now().replace(microsecond=0)
            amount = round(random.uniform(1000, 5000), 2)
            
            txn = {
                "transaction_id": f"T{random.randint(100000, 999999)}",
                "merchant_id": merchant_id,
                "customer_id": f"C{random.randint(1000, 9999)}",  # Different customer ID
                "timestamp": txn_time,
                "amount": amount,
                "status": "completed",
                "is_anomalous": True,
                "pattern": pattern
            }
            transactions.append(txn)

    return transactions
#Generate transactions for merchants


def generate_transactions_for_merchants(merchants):


    """Generate transactions for a given list of merchants."""
    total_merchants = len(merchants)
    num_normal = int(total_merchants * 0.8)  # 80% normal
    num_anomalous = total_merchants - num_normal  # Remaining 20% anomalous

    # Split merchants into normal and anomalous groups
    normal_merchants = merchants[:num_normal]
    anomalous_merchants = merchants[num_normal:]

 
    all_transactions = []
    for merchant in normal_merchants:
        # 80% normal transactions
        normal_txns = generate_normal_transactions(
            merchant_id=merchant["merchant_id"],
            amount_range=(100, 1000)
        )
        all_transactions.extend(normal_txns)

    # 20% anomalous transactions
    # Generate anomalous transactions
    for merchant in anomalous_merchants:
        anomaly_type = random.choice(["late_night", "high_velocity", "customer_concentration"])
        anomalous_txns = generate_anomalous_transactions(
            merchant_id=merchant["merchant_id"],
            pattern=anomaly_type
        )
        all_transactions.extend(anomalous_txns)
    return all_transactions



# # Example usage:
# merchants = generate_merchant_profiles(1000)  # Generate 1000 merchants
# transactions = generate_transactions_for_merchants(merchants)


def generate_dataset(num_merchants=1000):
    merchants = generate_merchant_profiles(num_merchants)
    transactions = generate_transactions_for_merchants(merchants)
    return transactions

# # Display example
# for txn in transactions[24000:24010]:
#    print(txn)