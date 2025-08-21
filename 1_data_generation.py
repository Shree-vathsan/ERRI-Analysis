import os
import pandas as pd
import numpy as np
from faker import Faker
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# --- Configuration ---
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "ecommerce_db"
CUSTOMER_COLLECTION = "customers"
ORDER_COLLECTION = "orders"

NUM_CUSTOMERS = 5000
NUM_ORDERS = 50000

fake = Faker()

# --- 1. Generate Synthetic Data ---
def generate_data():
    """Generates synthetic customer and order data using the Faker library."""
    print("Generating synthetic data...")
    # Generate Customers
    customers_data = []
    for i in range(NUM_CUSTOMERS):
        customers_data.append({
            "customer_id": 1000 + i,
            "name": fake.name(),
            "email": fake.email(),
            "signup_date": fake.date_time_between(start_date="-2y", end_date="now"),
            "marketing_channel": np.random.choice(["Social Media", "Organic Search", "Paid Ads", "Email"], p=[0.3, 0.4, 0.2, 0.1])
        })
    customers_df = pd.DataFrame(customers_data)
    
    # Generate Orders
    orders_data = []
    for _ in range(NUM_ORDERS):
        customer = customers_df.sample(1).iloc[0]
        order_date = fake.date_time_between(start_date=customer['signup_date'], end_date="now")
        orders_data.append({
            "order_id": fake.uuid4(),
            "customer_id": customer['customer_id'],
            "order_date": order_date,
            "order_value": round(np.random.uniform(20.0, 500.0), 2),
            "coupon_used": np.random.choice([True, False], p=[0.25, 0.75])
        })
    orders_df = pd.DataFrame(orders_data)
    print("Data generation complete.")
    return customers_df, orders_df

# --- 2. Load Data into MongoDB Atlas ---
def load_to_mongodb(customers_df, orders_df):
    """Connects to MongoDB and loads the DataFrames into collections."""
    print("Connecting to MongoDB Atlas...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # Drop existing collections to avoid duplicates on re-run
    db[CUSTOMER_COLLECTION].drop()
    db[ORDER_COLLECTION].drop()
    print(f"Dropped old collections in '{DB_NAME}' database.")
    
    # Convert DataFrames to dictionary records for MongoDB insertion
    customers_records = customers_df.to_dict('records')
    orders_records = orders_df.to_dict('records')
    
    # Insert data
    print(f"Inserting {len(customers_records)} customers...")
    db[CUSTOMER_COLLECTION].insert_many(customers_records)
    
    print(f"Inserting {len(orders_records)} orders...")
    db[ORDER_COLLECTION].insert_many(orders_records)
    
    print("Data loaded successfully to MongoDB Atlas!")
    client.close()

if __name__ == "__main__":
    customers, orders = generate_data()
    load_to_mongodb(customers, orders)