from __future__ import annotations

import re
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
RAW_PATH = DATA_DIR / "raw_sales_transactions.csv"
CLEAN_PATH = OUTPUT_DIR / "cleaned_sales_transactions.csv"
DICTIONARY_PATH = OUTPUT_DIR / "data_dictionary.md"
REPORT_PATH = OUTPUT_DIR / "quality_report.md"


PRODUCTS = [
    ("Wireless Mouse", "Electronics", 799.0),
    ("Bluetooth Speaker", "Electronics", 2499.0),
    ("Laptop Sleeve", "Electronics", 899.0),
    ("Coffee Mug", "Home & Kitchen", 299.0),
    ("Air Fryer", "Home & Kitchen", 8499.0),
    ("Bedsheet Set", "Home & Kitchen", 1199.0),
    ("Running Shoes", "Sports", 3499.0),
    ("Yoga Mat", "Sports", 699.0),
    ("Cricket Bat", "Sports", 1899.0),
    ("Notebook Pack", "Stationery", 249.0),
    ("Gel Pen Set", "Stationery", 149.0),
    ("Desk Organizer", "Stationery", 599.0),
]

CUSTOMERS = [
    ("C001", "Aarav Sharma", "aarav.sharma@example.com", "Ahmedabad", "1998-04-12"),
    ("C002", "Diya Mehta", "diya.mehta@example.com", "Mumbai", "1995-09-03"),
    ("C003", "Kabir Rao", "kabir.rao@example.com", "Delhi", "2001-01-27"),
    ("C004", "Meera Iyer", "meera.iyer@example.com", "Bengaluru", "1992-11-20"),
    ("C005", "Rohan Das", "rohan.das@example.com", "Kolkata", "1989-06-14"),
    ("C006", "Ananya Nair", "ananya.nair@example.com", "Kochi", "1999-12-05"),
    ("C007", "Ishaan Patel", "ishaan.patel@example.com", "Surat", "1994-07-18"),
    ("C008", "Sara Khan", "sara.khan@example.com", "Hyderabad", "1997-03-30"),
    ("C009", "Nikhil Verma", "nikhil.verma@example.com", "Pune", "1990-02-22"),
    ("C010", "Tara Singh", "tara.singh@example.com", "Chandigarh", "2000-10-09"),
]

CATEGORY_ALIASES = {
    "Electronics": ["Electronics", " electronics ", "electronic", "Elec"],
    "Home & Kitchen": ["Home & Kitchen", "home kitchen", "Kitchen", "HOME"],
    "Sports": ["Sports", "sports goods", "Sport", " sports "],
    "Stationery": ["Stationery", "stationary", "Office Supplies", " stationery "],
}

PAYMENT_ALIASES = [
    "Credit Card",
    "credit_card",
    "CARD",
    "UPI",
    "upi payment",
    "Cash",
    "COD",
    "Net Banking",
    "netbanking",
]

STATUS_ALIASES = ["Delivered", "complete", "Completed", "Returned", "refund", "cancel", "Cancelled"]
CHANNEL_ALIASES = ["Online", "online store", "Website", "Offline", "Retail", "Store"]


def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def format_mixed_date(value: datetime, index: int) -> str:
    if index % 23 == 0:
        return ""
    if index % 19 == 0:
        return "31-02-2025"
    if index % 13 == 0:
        return value.strftime("%d %b %Y")
    if index % 7 == 0:
        return value.strftime("%d/%m/%Y")
    return value.strftime("%Y-%m-%d")


def introduce_dirty_value(value: object, index: int, field: str) -> object:
    if field == "customer_id":
        if index % 29 == 0:
            return ""
        if index % 6 == 0:
            return f" {str(value).lower()} "
        return value

    if field == "customer_name":
        if index % 31 == 0:
            return ""
        if index % 5 == 0:
            return str(value).upper()
        if index % 9 == 0:
            return f"  {value}  "
        return value

    if field == "email":
        if index % 34 == 0:
            return ""
        if index % 17 == 0:
            return "invalid-email"
        if index % 8 == 0:
            return str(value).upper()
        return value

    if field == "dob":
        dob = datetime.strptime(str(value), "%Y-%m-%d")
        if index % 28 == 0:
            return ""
        if index % 11 == 0:
            return dob.strftime("%d/%m/%Y")
        if index % 16 == 0:
            return dob.strftime("%d %b %Y")
        return value

    return value


def generate_raw_dataset(path: Path) -> None:
    rng = np.random.default_rng(42)
    rows: list[dict[str, object]] = []
    start_date = datetime(2025, 1, 1)

    for i in range(1, 151):
        customer_id, customer_name, email, city, dob = CUSTOMERS[(i - 1) % len(CUSTOMERS)]
        product_name, category, price = PRODUCTS[(i * 3 + i // 4) % len(PRODUCTS)]
        order_date = start_date + timedelta(days=int(rng.integers(0, 181)))

        quantity: object = int(rng.integers(1, 5))
        if i % 31 == 0:
            quantity = ""
        elif i % 37 == 0:
            quantity = -2
        elif i % 43 == 0:
            quantity = 100

        unit_price: object = round(price * float(rng.uniform(0.92, 1.08)), 2)
        if i % 18 == 0:
            unit_price = f"INR {unit_price:,.2f}"
        elif i % 22 == 0:
            unit_price = f"Rs. {unit_price:,.0f}"
        elif i % 41 == 0:
            unit_price = "free"
        elif i % 47 == 0:
            unit_price = 99999

        discount_pct: object = float(rng.choice([0, 0.05, 0.10, 0.15]))
        if i % 10 == 0:
            discount_pct = "10%"
        elif i % 24 == 0:
            discount_pct = ""
        elif i % 39 == 0:
            discount_pct = "75%"

        row = {
            "transaction_id": f"T{i + 1000}",
            "order_date": format_mixed_date(order_date, i),
            "customer_id": introduce_dirty_value(customer_id, i, "customer_id"),
            "customer_name": introduce_dirty_value(customer_name, i, "customer_name"),
            "email": introduce_dirty_value(email, i, "email"),
            "date_of_birth": introduce_dirty_value(dob, i, "dob"),
            "city": city.upper() if i % 12 == 0 else f" {city} " if i % 8 == 0 else city,
            "product_category": rng.choice(CATEGORY_ALIASES[category]),
            "product_name": product_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_pct": discount_pct,
            "payment_method": rng.choice(PAYMENT_ALIASES),
            "order_status": rng.choice(STATUS_ALIASES),
            "sales_channel": rng.choice(CHANNEL_ALIASES),
        }
        rows.append(row)

    rows.append(rows[8].copy())
    rows.append(rows[19].copy())

    duplicate_with_changes = rows[49].copy()
    duplicate_with_changes["customer_name"] = "  " + str(duplicate_with_changes["customer_name"]).lower()
    duplicate_with_changes["discount_pct"] = "5%"
    duplicate_with_changes["sales_channel"] = "website"
    rows.append(duplicate_with_changes)

    missing_id_row = rows[69].copy()
    missing_id_row["transaction_id"] = ""
    missing_id_row["email"] = "missing.id@example.com"
    rows.append(missing_id_row)

    pd.DataFrame(rows).to_csv(path, index=False)


def normalize_key(value: object) -> str:
    text = "" if pd.isna(value) else str(value).strip().lower()
    return re.sub(r"[^a-z0-9]+", "", text)


def normalize_name(value: object) -> str:
    text = "" if pd.isna(value) else str(value).strip()
    return "Unknown" if not text else re.sub(r"\s+", " ", text).title()


def normalize_id(value: object, prefix: str, row_number: int) -> str:
    text = "" if pd.isna(value) else str(value).strip().upper()
    text = re.sub(r"\s+", "", text)
    return text if text else f"{prefix}_GENERATED_{row_number:04d}"


def parse_date(value: object) -> pd.Timestamp:
    if pd.isna(value):
        return pd.NaT

    text = str(value).strip()
    if not text:
        return pd.NaT

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%d %B %Y"):
        try:
            return pd.Timestamp(datetime.strptime(text, fmt))
        except ValueError:
            continue

    return pd.to_datetime(text, errors="coerce", dayfirst=True)


def parse_money(value: object) -> float:
    if pd.isna(value):
        return np.nan

    cleaned = re.sub(r"[^0-9.\-]", "", str(value).replace(",", ""))
    if cleaned in {"", "-", "."}:
        return np.nan

    try:
        return float(cleaned)
    except ValueError:
        return np.nan


def parse_discount(value: object) -> float:
    if pd.isna(value):
        return 0.0

    raw = str(value).strip()
    if not raw:
        return 0.0

    cleaned = re.sub(r"[^0-9.\-]", "", raw)
    if not cleaned:
        return 0.0

    try:
        discount = float(cleaned)
    except ValueError:
        return 0.0

    if "%" in raw or discount > 1:
        discount = discount / 100

    return float(min(max(discount, 0.0), 0.50))


CATEGORY_MAP = {
    "electronics": "Electronics",
    "electronic": "Electronics",
    "elec": "Electronics",
    "homekitchen": "Home & Kitchen",
    "kitchen": "Home & Kitchen",
    "home": "Home & Kitchen",
    "sports": "Sports",
    "sport": "Sports",
    "sportsgoods": "Sports",
    "stationery": "Stationery",
    "stationary": "Stationery",
    "officesupplies": "Stationery",
}

PAYMENT_MAP = {
    "creditcard": "Card",
    "card": "Card",
    "upi": "UPI",
    "upipayment": "UPI",
    "cash": "Cash",
    "cod": "Cash",
    "netbanking": "Net Banking",
}

STATUS_MAP = {
    "delivered": "Delivered",
    "complete": "Delivered",
    "completed": "Delivered",
    "returned": "Returned",
    "refund": "Returned",
    "cancel": "Cancelled",
    "cancelled": "Cancelled",
}

CHANNEL_MAP = {
    "online": "Online",
    "onlinestore": "Online",
    "website": "Online",
    "offline": "Offline",
    "retail": "Offline",
    "store": "Offline",
}


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    def cell(value: object) -> str:
        return "" if pd.isna(value) else str(value).replace("\n", " ")

    widths = [len(header) for header in headers]
    prepared = [[cell(value) for value in row] for row in rows]
    for row in prepared:
        widths = [max(width, len(value)) for width, value in zip(widths, row)]

    header_line = "| " + " | ".join(header.ljust(width) for header, width in zip(headers, widths)) + " |"
    divider = "| " + " | ".join("-" * width for width in widths) + " |"
    body = ["| " + " | ".join(value.ljust(width) for value, width in zip(row, widths)) + " |" for row in prepared]
    return "\n".join([header_line, divider, *body])


def missing_summary(df: pd.DataFrame) -> pd.Series:
    normalized = df.replace(r"^\s*$", np.nan, regex=True)
    return normalized.isna().sum().sort_values(ascending=False)


def build_quality_report(raw: pd.DataFrame, cleaned: pd.DataFrame, actions: dict[str, int]) -> str:
    missing_rows = [[col, int(count)] for col, count in missing_summary(raw).items()]
    action_rows = [[name.replace("_", " ").title(), count] for name, count in actions.items()]
    final_missing_rows = [[col, int(count)] for col, count in missing_summary(cleaned).items() if int(count) > 0]

    category_rows = (
        cleaned.groupby("product_category", dropna=False)
        .agg(orders=("transaction_id", "count"), net_sales=("net_sales", "sum"))
        .reset_index()
        .sort_values("net_sales", ascending=False)
    )
    category_table = [
        [row.product_category, int(row.orders), f"{row.net_sales:.2f}"] for row in category_rows.itertuples()
    ]

    status_rows = (
        cleaned.groupby("order_status", dropna=False)
        .agg(orders=("transaction_id", "count"), net_sales=("net_sales", "sum"))
        .reset_index()
        .sort_values("orders", ascending=False)
    )
    status_table = [[row.order_status, int(row.orders), f"{row.net_sales:.2f}"] for row in status_rows.itertuples()]

    final_missing_table = (
        markdown_table(["Column", "Remaining Missing Values"], final_missing_rows)
        if final_missing_rows
        else "No remaining missing values in required analysis columns. Optional emails and dates are blank only when unavailable."
    )

    return f"""# Task 1 Quality Assessment Report

## Dataset Overview

- Raw dataset: `{RAW_PATH.name}`
- Cleaned dataset: `{CLEAN_PATH.name}`
- Raw rows: {len(raw)}
- Cleaned rows: {len(cleaned)}
- Raw columns: {len(raw.columns)}
- Cleaned columns: {len(cleaned.columns)}
- Cleaned date range: {cleaned["order_date"].min()} to {cleaned["order_date"].max()}
- Total cleaned net sales: {cleaned["net_sales"].sum():.2f}

## Initial Profiling Findings

- Exact duplicate rows found: {int(raw.duplicated().sum())}
- Duplicate transaction IDs found: {int(raw["transaction_id"].replace(r"^\\s*$", np.nan, regex=True).duplicated().sum())}
- Mixed date formats were present in `order_date` and `date_of_birth`.
- Free-text categories were inconsistent across product category, payment method, order status, sales channel, and city.
- Numeric fields included currency symbols, blanks, negative quantities, extreme quantities, and unrealistic unit prices.

## Missing Values Before Cleaning

{markdown_table(["Column", "Missing Values"], missing_rows)}

## Cleaning Actions Applied

{markdown_table(["Action", "Rows Affected"], action_rows)}

## Remaining Missing Values After Cleaning

{final_missing_table}

## Category Summary After Cleaning

{markdown_table(["Product Category", "Orders", "Net Sales"], category_table)}

## Order Status Summary After Cleaning

{markdown_table(["Order Status", "Orders", "Net Sales"], status_table)}

## Notes For Submission Video

1. Show the raw file and point out missing values, duplicates, inconsistent text labels, mixed dates, and invalid numeric values.
2. Open `clean_sales_data.py` and explain the cleaning functions for dates, currency, discounts, categories, and duplicate transaction IDs.
3. Show `cleaned_sales_transactions.csv` and highlight the new columns: `order_month`, `customer_age`, `gross_sales`, `net_sales`, and `is_returned`.
"""


def build_data_dictionary() -> str:
    rows = [
        ["transaction_id", "String", "Unique order identifier", "Primary key for order-level analysis", "Generated when missing; duplicate IDs deduplicated"],
        ["order_date", "Date", "Date the order was placed", "Supports trend and seasonality analysis", "Parsed to ISO `YYYY-MM-DD`; invalid dates removed"],
        ["order_month", "String", "Month extracted from order date", "Monthly revenue and order volume tracking", "Derived as `YYYY-MM`"],
        ["customer_id", "String", "Unique customer identifier", "Customer repeat behavior and segmentation", "Trimmed, uppercased, generated when missing"],
        ["customer_name", "String", "Customer full name", "Customer reference field", "Trimmed and title-cased; missing set to Unknown"],
        ["email", "String", "Customer email address", "Optional contact and CRM matching", "Lowercased; invalid emails blanked"],
        ["date_of_birth", "Date", "Customer birth date", "Age-based segmentation", "Parsed to ISO date when valid"],
        ["customer_age", "Integer", "Customer age at time of order", "Demographic analysis", "Derived from date of birth and order date; unreasonable ages blanked"],
        ["city", "String", "Customer city", "Geographic sales comparison", "Trimmed and title-cased"],
        ["product_category", "String", "Standard product category", "Category-level sales and margin analysis", "Mapped from inconsistent free-text labels"],
        ["product_name", "String", "Product purchased", "Product performance analysis", "Trimmed and normalized spacing"],
        ["quantity", "Integer", "Units purchased", "Volume and basket-size analysis", "Invalid values filled; high outliers capped at 20"],
        ["unit_price", "Decimal", "Selling price per unit", "Revenue calculation", "Currency symbols removed; invalid/outlier values imputed"],
        ["discount_pct", "Decimal", "Discount as a 0-0.50 proportion", "Promotion impact analysis", "Percent strings converted; values capped at 50%"],
        ["gross_sales", "Decimal", "Quantity multiplied by unit price", "Pre-discount revenue", "Derived field"],
        ["net_sales", "Decimal", "Revenue after discount", "Primary sales KPI", "Derived field"],
        ["payment_method", "String", "Standardized payment method", "Payment behavior analysis", "Mapped to Card, UPI, Cash, Net Banking, or Other"],
        ["order_status", "String", "Standardized order status", "Fulfillment and cancellation analysis", "Mapped to Delivered, Returned, Cancelled, or Other"],
        ["sales_channel", "String", "Online or Offline channel", "Channel performance analysis", "Mapped from website/store/free-text values"],
        ["is_returned", "Boolean", "Whether the order was returned", "Return-rate tracking", "Derived from order status"],
    ]

    return f"""# Task 1 Data Dictionary

Dataset: `cleaned_sales_transactions.csv`

{markdown_table(["Column", "Type", "Meaning", "Business Relevance", "Cleaning / Transformation"], rows)}
"""


def clean_dataset(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    df = raw.copy()
    raw_columns = list(df.columns)
    exact_duplicates = int(df.duplicated(subset=raw_columns).sum())
    df = df.drop_duplicates(subset=raw_columns).copy()
    df["raw_row_number"] = np.arange(1, len(df) + 1)

    actions: dict[str, int] = {
        "exact_duplicates_removed": exact_duplicates,
        "missing_transaction_ids_generated": int(df["transaction_id"].replace(r"^\s*$", np.nan, regex=True).isna().sum()),
        "invalid_order_dates_removed": 0,
        "invalid_emails_blanked": 0,
        "invalid_quantities_imputed": 0,
        "quantity_outliers_capped": 0,
        "invalid_unit_prices_imputed": 0,
        "unit_price_outliers_imputed": 0,
        "duplicate_transaction_ids_removed": 0,
    }

    df["transaction_id"] = [
        normalize_id(value, "TXN", row_number) for value, row_number in zip(df["transaction_id"], df["raw_row_number"])
    ]
    df["customer_id"] = [
        normalize_id(value, "CUST", row_number) for value, row_number in zip(df["customer_id"], df["raw_row_number"])
    ]

    df["customer_name"] = df["customer_name"].map(normalize_name)
    df["email"] = df["email"].map(lambda value: "" if pd.isna(value) else str(value).strip().lower())
    email_valid = df["email"].eq("") | df["email"].str.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", na=False)
    actions["invalid_emails_blanked"] = int((~email_valid).sum())
    df.loc[~email_valid, "email"] = ""

    df["order_date"] = df["order_date"].map(parse_date)
    df["date_of_birth"] = df["date_of_birth"].map(parse_date)
    actions["invalid_order_dates_removed"] = int(df["order_date"].isna().sum())
    df = df[df["order_date"].notna()].copy()

    df["city"] = df["city"].map(lambda value: normalize_name(value))
    df["product_name"] = df["product_name"].map(lambda value: re.sub(r"\s+", " ", str(value).strip()).title())
    df["product_category"] = df["product_category"].map(lambda value: CATEGORY_MAP.get(normalize_key(value), "Other"))
    df["payment_method"] = df["payment_method"].map(lambda value: PAYMENT_MAP.get(normalize_key(value), "Other"))
    df["order_status"] = df["order_status"].map(lambda value: STATUS_MAP.get(normalize_key(value), "Other"))
    df["sales_channel"] = df["sales_channel"].map(lambda value: CHANNEL_MAP.get(normalize_key(value), "Other"))

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    invalid_quantity = df["quantity"].isna() | (df["quantity"] <= 0)
    actions["invalid_quantities_imputed"] = int(invalid_quantity.sum())
    df.loc[invalid_quantity, "quantity"] = 1
    quantity_outliers = df["quantity"] > 20
    actions["quantity_outliers_capped"] = int(quantity_outliers.sum())
    df.loc[quantity_outliers, "quantity"] = 20
    df["quantity"] = df["quantity"].astype(int)

    df["unit_price"] = df["unit_price"].map(parse_money)
    invalid_unit_price = df["unit_price"].isna() | (df["unit_price"] <= 0)
    actions["invalid_unit_prices_imputed"] = int(invalid_unit_price.sum())

    unit_price_outliers = df["unit_price"] > 50000
    actions["unit_price_outliers_imputed"] = int(unit_price_outliers.sum())
    df.loc[unit_price_outliers, "unit_price"] = np.nan

    product_medians = df.groupby("product_name")["unit_price"].transform("median")
    category_medians = df.groupby("product_category")["unit_price"].transform("median")
    global_median = df["unit_price"].median()
    df["unit_price"] = df["unit_price"].fillna(product_medians).fillna(category_medians).fillna(global_median).round(2)

    df["discount_pct"] = df["discount_pct"].map(parse_discount).round(2)
    df["gross_sales"] = (df["quantity"] * df["unit_price"]).round(2)
    df["net_sales"] = (df["gross_sales"] * (1 - df["discount_pct"])).round(2)
    df["is_returned"] = df["order_status"].eq("Returned")
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

    age = ((df["order_date"] - df["date_of_birth"]).dt.days / 365.25).astype("float")
    df["customer_age"] = age.where(age.between(13, 90)).round()

    completeness_cols = [
        "order_date",
        "customer_id",
        "customer_name",
        "product_category",
        "quantity",
        "unit_price",
        "payment_method",
        "order_status",
        "sales_channel",
    ]
    df["completeness_score"] = df[completeness_cols].notna().sum(axis=1) + df[completeness_cols].ne("").sum(axis=1)
    before_id_dedupe = len(df)
    df = (
        df.sort_values(["transaction_id", "completeness_score", "raw_row_number"], ascending=[True, False, True])
        .drop_duplicates(subset=["transaction_id"], keep="first")
        .copy()
    )
    actions["duplicate_transaction_ids_removed"] = before_id_dedupe - len(df)

    output_columns = [
        "transaction_id",
        "order_date",
        "order_month",
        "customer_id",
        "customer_name",
        "email",
        "date_of_birth",
        "customer_age",
        "city",
        "product_category",
        "product_name",
        "quantity",
        "unit_price",
        "discount_pct",
        "gross_sales",
        "net_sales",
        "payment_method",
        "order_status",
        "sales_channel",
        "is_returned",
    ]
    df = df[output_columns].sort_values("order_date").reset_index(drop=True)

    for col in ("order_date", "date_of_birth"):
        df[col] = df[col].dt.strftime("%Y-%m-%d").fillna("")

    df["customer_age"] = df["customer_age"].astype("Int64")
    return df, actions


def main() -> None:
    ensure_dirs()

    if not RAW_PATH.exists():
        generate_raw_dataset(RAW_PATH)

    raw = pd.read_csv(RAW_PATH, keep_default_na=False)
    cleaned, actions = clean_dataset(raw)

    cleaned.to_csv(CLEAN_PATH, index=False)
    DICTIONARY_PATH.write_text(build_data_dictionary(), encoding="utf-8")
    REPORT_PATH.write_text(build_quality_report(raw, cleaned, actions), encoding="utf-8")

    print(f"Raw dataset: {RAW_PATH}")
    print(f"Cleaned dataset: {CLEAN_PATH}")
    print(f"Data dictionary: {DICTIONARY_PATH}")
    print(f"Quality report: {REPORT_PATH}")
    print(f"Rows: raw={len(raw)}, cleaned={len(cleaned)}")


if __name__ == "__main__":
    main()
