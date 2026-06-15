# Task 1 Data Dictionary

Dataset: `cleaned_sales_transactions.csv`

| Column           | Type    | Meaning                           | Business Relevance                        | Cleaning / Transformation                                            |
| ---------------- | ------- | --------------------------------- | ----------------------------------------- | -------------------------------------------------------------------- |
| transaction_id   | String  | Unique order identifier           | Primary key for order-level analysis      | Generated when missing; duplicate IDs deduplicated                   |
| order_date       | Date    | Date the order was placed         | Supports trend and seasonality analysis   | Parsed to ISO `YYYY-MM-DD`; invalid dates removed                    |
| order_month      | String  | Month extracted from order date   | Monthly revenue and order volume tracking | Derived as `YYYY-MM`                                                 |
| customer_id      | String  | Unique customer identifier        | Customer repeat behavior and segmentation | Trimmed, uppercased, generated when missing                          |
| customer_name    | String  | Customer full name                | Customer reference field                  | Trimmed and title-cased; missing set to Unknown                      |
| email            | String  | Customer email address            | Optional contact and CRM matching         | Lowercased; invalid emails blanked                                   |
| date_of_birth    | Date    | Customer birth date               | Age-based segmentation                    | Parsed to ISO date when valid                                        |
| customer_age     | Integer | Customer age at time of order     | Demographic analysis                      | Derived from date of birth and order date; unreasonable ages blanked |
| city             | String  | Customer city                     | Geographic sales comparison               | Trimmed and title-cased                                              |
| product_category | String  | Standard product category         | Category-level sales and margin analysis  | Mapped from inconsistent free-text labels                            |
| product_name     | String  | Product purchased                 | Product performance analysis              | Trimmed and normalized spacing                                       |
| quantity         | Integer | Units purchased                   | Volume and basket-size analysis           | Invalid values filled; high outliers capped at 20                    |
| unit_price       | Decimal | Selling price per unit            | Revenue calculation                       | Currency symbols removed; invalid/outlier values imputed             |
| discount_pct     | Decimal | Discount as a 0-0.50 proportion   | Promotion impact analysis                 | Percent strings converted; values capped at 50%                      |
| gross_sales      | Decimal | Quantity multiplied by unit price | Pre-discount revenue                      | Derived field                                                        |
| net_sales        | Decimal | Revenue after discount            | Primary sales KPI                         | Derived field                                                        |
| payment_method   | String  | Standardized payment method       | Payment behavior analysis                 | Mapped to Card, UPI, Cash, Net Banking, or Other                     |
| order_status     | String  | Standardized order status         | Fulfillment and cancellation analysis     | Mapped to Delivered, Returned, Cancelled, or Other                   |
| sales_channel    | String  | Online or Offline channel         | Channel performance analysis              | Mapped from website/store/free-text values                           |
| is_returned      | Boolean | Whether the order was returned    | Return-rate tracking                      | Derived from order status                                            |
