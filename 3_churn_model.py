import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def train_churn_model(data_path="data/rfm_analysis.csv"):
    """Loads RFM data, defines churn, and trains a logistic regression model."""
    try:
        rfm_df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: The file {data_path} was not found. Please run '2_data_analysis.py' first.")
        return

    # --- 1. Feature Engineering & Churn Definition ---
    # Define churn: A customer is considered "churned" if their last purchase
    # was more than 90 days ago (high recency value).
    CHURN_THRESHOLD_DAYS = 90
    rfm_df['Churn'] = rfm_df['Recency'].apply(lambda x: 1 if x > CHURN_THRESHOLD_DAYS else 0)

    print("--- Churn Prediction Model ---")
    print(f"Churn defined as no purchase in the last {CHURN_THRESHOLD_DAYS} days.")
    print(f"Churn Distribution:\n{rfm_df['Churn'].value_counts(normalize=True)}\n")

    # --- 2. Model Building ---
    # Select features and target variable
    features = ['Recency', 'Frequency', 'Monetary']
    X = rfm_df[features]
    y = rfm_df['Churn']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Initialize and train the Logistic Regression model
    model = LogisticRegression(random_state=42)
    print("Training the model...")
    model.fit(X_train, y_train)
    print("Model training complete.")

    # --- 3. Model Evaluation ---
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Print key metrics
    print("\n--- Model Evaluation ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Not Churned', 'Churned']))

    # Visualize the Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Not Churned', 'Churned'], yticklabels=['Not Churned', 'Churned'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.show()

if __name__ == "__main__":
    train_churn_model()