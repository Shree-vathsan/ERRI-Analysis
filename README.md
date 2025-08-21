# E-Commerce Pulse: Predictive Revenue & Retention Engine

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Database](https://img.shields.io/badge/Database-MongoDB-green.svg)
![Visualization](https://img.shields.io/badge/Visualization-Power%20BI-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)

An end-to-end analytics project to track e-commerce revenue, analyze customer retention, and predict customer churn using Python, MongoDB, and Power BI.

## 📊 Dashboard Preview

Below is a preview of the final Power BI dashboard, which provides a comprehensive overview of key business metrics and customer insights.

**_-- INSERT YOUR POWER BI DASHBOARD SCREENSHOT HERE --_**


## ## 🎯 Project Overview

E-commerce businesses often struggle with customer churn and poor visibility into the key drivers of revenue. This project addresses this by building a full-stack data solution that ingests, analyzes, and visualizes customer transaction data. The core goal is to move from raw data to actionable business intelligence, enabling data-driven decisions to boost revenue and retention.

### ## ✨ Key Features

* **RFM Customer Segmentation:** Automatically segments customers into meaningful categories like 'Champions', 'At Risk', and 'Hibernating' based on their Recency, Frequency, and Monetary behavior.
* **Cohort Retention Analysis:** Tracks customer cohorts over time to measure long-term engagement and calculate monthly retention rates.
* **Predictive Churn Modeling:** Utilizes a Logistic Regression model to predict the likelihood of a customer churning, achieving over 99% accuracy on the dataset.
* **Interactive BI Dashboard:** A multi-page Power BI dashboard that visualizes KPIs, segmentation, and retention trends for business stakeholders.
* **Business Documentation:** Includes a Business Requirement Document (BRD) and a KPI Dictionary, bridging the gap between technical implementation and business objectives.

## ## 🛠️ Tech Stack

| Component | Technology / Library |
| :--- | :--- |
| **Data Generation & Analysis** | Python (Pandas, NumPy, Faker) |
| **Database** | MongoDB Atlas (NoSQL) |
| **Machine Learning** | Scikit-learn |
| **Data Visualization** | Power BI, Matplotlib, Seaborn |
| **Environment Management** | `venv`, `python-dotenv` |

## ## 🏗️ Project Architecture

The project follows a simple, robust data pipeline:

1.  **Data Generation:** A Python script generates a synthetic dataset of 5,000 customers and 50,000+ orders.
2.  **Data Storage:** The generated data is loaded into a **MongoDB Atlas** cloud database.
3.  **Analysis & Modeling:** A second Python script pulls data from MongoDB, performs RFM and cohort analysis, and trains a churn model.
4.  **Data Export:** The aggregated insights are saved as `.csv` files.
5.  **Visualization:** **Power BI** connects to the CSV files to create the final interactive dashboard.

## ## ⚙️ Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/Your-Repository-Name.git](https://github.com/your-username/Your-Repository-Name.git)
    cd Your-Repository-Name
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    * Create a file named `.env` in the root directory.
    * Add your MongoDB Atlas connection string to this file:
        ```env
        MONGO_URI="mongodb+srv://<username>:<password>@yourcluster.mongodb.net/?retryWrites=true&w=majority"
        ```

## ## 🚀 How to Run

Execute the scripts from your terminal in the following order:

1.  **Generate and Load Data into MongoDB:**
    ```bash
    python 1_data_generation.py
    ```

2.  **Perform Analysis and Create CSV Files:**
    ```bash
    python 2_data_analysis.py
    ```

3.  **Train and Evaluate the Churn Model:**
    ```bash
    python 3_churn_model.py
    ```

After running these scripts, the `data/` folder will contain the `rfm_analysis.csv` and `cohort_retention.csv` files, which can be used as the data source for the Power BI dashboard.

## ## 📄 Business Deliverables

This project also includes key business analysis documents located in the `/docs` folder:

* **`BRD.md`**: A Business Requirement Document outlining the project's goals, scope, and objectives.
* **`KPI_Dictionary.md`**: A clear dictionary defining all the key metrics used in the analysis.
