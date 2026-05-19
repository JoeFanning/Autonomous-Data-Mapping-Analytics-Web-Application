import pandas as pd


def process_analytics(df, sales_column):
    """
    Safely parses the data and returns dictionary statistics or raising errors.
    """
    # Force convert to numeric, making strings/dates invalid as NaN
    numeric_sales = pd.to_numeric(df[sales_column], errors='coerce')

    # Check if column is completely devoid of math numbers
    if numeric_sales.dropna().empty:
        raise ValueError(f"'{sales_column}' does not contain numbers. Choose a numeric column.")

    metrics = {
        "total_sales": float(numeric_sales.sum()),
        "average_sales": float(numeric_sales.mean()),
        "row_count": int(len(df))
    }
    return metrics
