# Task 1 Quality Assessment Report

## Dataset Overview

- Raw dataset: `raw_sales_transactions.csv`
- Cleaned dataset: `cleaned_sales_transactions.csv`
- Raw rows: 154
- Cleaned rows: 138
- Raw columns: 15
- Cleaned columns: 20
- Cleaned date range: 2025-01-01 to 2025-06-30
- Total cleaned net sales: 630195.86

## Initial Profiling Findings

- Exact duplicate rows found: 2
- Duplicate transaction IDs found: 3
- Mixed date formats were present in `order_date` and `date_of_birth`.
- Free-text categories were inconsistent across product category, payment method, order status, sales channel, and city.
- Numeric fields included currency symbols, blanks, negative quantities, extreme quantities, and unrealistic unit prices.

## Missing Values Before Cleaning

| Column           | Missing Values |
| ---------------- | -------------- |
| order_date       | 6              |
| customer_id      | 5              |
| date_of_birth    | 5              |
| discount_pct     | 5              |
| email            | 4              |
| quantity         | 4              |
| customer_name    | 4              |
| transaction_id   | 1              |
| city             | 0              |
| product_name     | 0              |
| product_category | 0              |
| unit_price       | 0              |
| payment_method   | 0              |
| order_status     | 0              |
| sales_channel    | 0              |

## Cleaning Actions Applied

| Action                            | Rows Affected |
| --------------------------------- | ------------- |
| Exact Duplicates Removed          | 2             |
| Missing Transaction Ids Generated | 1             |
| Invalid Order Dates Removed       | 13            |
| Invalid Emails Blanked            | 4             |
| Invalid Quantities Imputed        | 8             |
| Quantity Outliers Capped          | 3             |
| Invalid Unit Prices Imputed       | 3             |
| Unit Price Outliers Imputed       | 3             |
| Duplicate Transaction Ids Removed | 1             |

## Remaining Missing Values After Cleaning

| Column        | Remaining Missing Values |
| ------------- | ------------------------ |
| email         | 8                        |
| date_of_birth | 5                        |
| customer_age  | 5                        |

## Category Summary After Cleaning

| Product Category | Orders | Net Sales |
| ---------------- | ------ | --------- |
| Home & Kitchen   | 34     | 298889.06 |
| Sports           | 35     | 183818.91 |
| Electronics      | 33     | 115663.90 |
| Stationery       | 36     | 31823.99  |

## Order Status Summary After Cleaning

| Order Status | Orders | Net Sales |
| ------------ | ------ | --------- |
| Delivered    | 60     | 320834.34 |
| Cancelled    | 39     | 187489.16 |
| Returned     | 39     | 121872.36 |

## Notes For Submission Video

1. Show the raw file and point out missing values, duplicates, inconsistent text labels, mixed dates, and invalid numeric values.
2. Open `clean_sales_data.py` and explain the cleaning functions for dates, currency, discounts, categories, and duplicate transaction IDs.
3. Show `cleaned_sales_transactions.csv` and highlight the new columns: `order_month`, `customer_age`, `gross_sales`, `net_sales`, and `is_returned`.
