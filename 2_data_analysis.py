import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# --- Configuration & Connection ---
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "ecommerce_db"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# --- 1. Load Data from MongoDB into Pandas ---
def load_data_from_mongo():
    """Fetches customer and order data from MongoDB and returns them as pandas DataFrames."""
    print("Loading data from MongoDB...")
    customers_cursor = db.customers.find({})
    orders_cursor = db.orders.find({})
    
    customers_df = pd.DataFrame(list(customers_cursor))
    orders_df = pd.DataFrame(list(orders_cursor))

    # Basic data type conversion
    customers_df['signup_date'] = pd.to_datetime(customers_df['signup_date'])
    orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
    
    print("Data loaded and converted successfully.")
    return customers_df, orders_df

# --- 2. RFM (Recency, Frequency, Monetary) Analysis ---
def perform_rfm_analysis(df):
    """Calculates RFM scores and segments customers."""
    print("\n--- Performing RFM Analysis ---")
    snapshot_date = df['order_date'].max() + pd.Timedelta(days=1)
    
    rfm_data = df.groupby('customer_id').agg({
        'order_date': lambda x: (snapshot_date - x.max()).days, # Recency
        'order_id': 'count', # Frequency
        'order_value': 'sum' # Monetary
    }).rename(columns={'order_date': 'Recency', 'order_id': 'Frequency', 'order_value': 'Monetary'})

    # Create RFM quantiles and scores (1 is worst, 5 is best)
    rfm_data['R_score'] = pd.qcut(rfm_data['Recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm_data['F_score'] = pd.qcut(rfm_data['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm_data['M_score'] = pd.qcut(rfm_data['Monetary'], 5, labels=[1, 2, 3, 4, 5])
    
    # Define customer segments based on R and F scores
    segment_map = {
        r'[1-2][1-2]': 'Hibernating',
        r'[1-2][3-4]': 'At Risk',
        r'[1-2]5': 'Cannot Lose Them',
        r'3[1-2]': 'About to Sleep',
        r'33': 'Need Attention',
        r'[3-4][4-5]': 'Loyal Customers',
        r'41': 'Promising',
        r'51': 'New Customers',
        r'[4-5][2-3]': 'Potential Loyalists',
        r'5[4-5]': 'Champions'
    }
    rfm_data['Segment'] = rfm_data['R_score'].astype(str) + rfm_data['F_score'].astype(str)
    rfm_data['Segment'] = rfm_data['Segment'].replace(segment_map, regex=True)

    print("RFM Analysis Complete.")
    return rfm_data

# --- 3. Cohort Analysis (Customer Retention) ---
def perform_cohort_analysis(customers_df, orders_df):
    """Calculates monthly cohort retention rates."""
    print("\n--- Performing Cohort Analysis ---")
    df = pd.merge(orders_df, customers_df[['customer_id', 'signup_date']], on='customer_id')
    
    def get_month(x): return datetime(x.year, x.month, 1)

    df['OrderMonth'] = df['order_date'].apply(get_month)
    df['CohortMonth'] = df['signup_date'].apply(get_month)
    
    def get_cohort_index(df):
        year_diff = df['OrderMonth'].dt.year - df['CohortMonth'].dt.year
        month_diff = df['OrderMonth'].dt.month - df['CohortMonth'].dt.month
        return year_diff * 12 + month_diff + 1

    df['CohortIndex'] = get_cohort_index(df)

    cohort_data = df.groupby(['CohortMonth', 'CohortIndex'])['customer_id'].apply(pd.Series.nunique).reset_index()
    cohort_counts = cohort_data.pivot_table(index='CohortMonth', columns='CohortIndex', values='customer_id')
    
    # Calculate retention rate as a percentage
    cohort_sizes = cohort_counts.iloc[:, 0]
    retention_matrix = cohort_counts.divide(cohort_sizes, axis=0)
    retention_matrix = (retention_matrix * 100).round(1)

    print("Cohort Analysis Complete.")
    return retention_matrix

# --- Main Execution ---
if __name__ == "__main__":
    customers, orders = load_data_from_mongo()
    
    # Perform analyses
    rfm_results = perform_rfm_analysis(orders)
    cohort_results = perform_cohort_analysis(customers, orders)
    
    # Save results to CSV files in the 'data' directory
    if not os.path.exists('data'):
        os.makedirs('data')
        
    rfm_path = "data/rfm_analysis.csv"
    cohort_path = "data/cohort_retention.csv"
    
    rfm_results.to_csv(rfm_path)
    cohort_results.to_csv(cohort_path)
    
    print(f"\nAnalysis results saved to '{rfm_path}' and '{cohort_path}'")
    client.close()