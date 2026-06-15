# Task 1: Data Immersion and Wrangling

This folder contains a complete Task 1 submission package based on the internship PDF:

- `data/raw_sales_transactions.csv` - raw sales transaction dataset with realistic data-quality issues.
- `clean_sales_data.py` - Pandas script that profiles, cleans, transforms, and exports the analysis-ready dataset.
- `output/cleaned_sales_transactions.csv` - final cleaned dataset.
- `output/data_dictionary.md` - variable definitions, data types, business relevance, and transformation notes.
- `output/quality_report.md` - before/after profiling summary and cleaning actions.

## How To Run

```powershell
py -3 -m pip install pandas numpy
py -3 task1_data_wrangling\clean_sales_data.py
```

If you want to use a real internship dataset later, replace `data/raw_sales_transactions.csv` with the same column structure and rerun the script.
