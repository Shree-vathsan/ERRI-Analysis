# KPI Dictionary for the ERRI Project

This document provides clear definitions and formulas for all Key Performance Indicators (KPIs) used in the analytics dashboard.

| KPI Name | Definition | Formula / Calculation | Data Source(s) |
| :--- | :--- | :--- | :--- |
| **Revenue** | The total monetary value of all completed orders within a given period. | `SUM(order_value)` | `orders` collection |
| **Orders** | The total count of all completed orders within a given period. | `COUNT(order_id)` | `orders` collection |
| **Average Order Value (AOV)** | The average amount a customer spends per transaction. | `Total Revenue / Total Orders` | `orders` collection |
| **Customer Count** | The total number of unique customers who have signed up. | `COUNT(DISTINCT customer_id)` | `customers` collection |
| **Churn Rate (%)** | The percentage of customers who are considered "churned" (inactive) based on a defined threshold. | `(Number of Churned Customers / Total Customers) * 100` | RFM Analysis Logic |
| **Recency** | The number of days since a customer's last purchase. | `(Snapshot Date - Last Order Date)` | `orders` collection |
| **Frequency** | The total number of orders a customer has placed. | `COUNT(order_id) per customer` | `orders` collection |
| **Monetary Value** | The total revenue generated from a single customer. | `SUM(order_value) per customer` | `orders` collection |
| **Cohort Retention (%)** | The percentage of customers from a specific signup cohort who return to make a purchase in subsequent months. | `(Active Customers in Month N / Total Customers in Cohort) * 100` | Cohort Analysis Logic |