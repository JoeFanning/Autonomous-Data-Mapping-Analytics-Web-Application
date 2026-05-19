import pandas as pd
import streamlit as st


@st.cache_data(show_spinner="Combining and formatting files...")
def load_and_combine_data(files) -> pd.DataFrame:
    """
    Parses uploaded CSV or Excel files and merges them into a single DataFrame.
    Optimized with st.cache_data to prevent repetitive disk reads.
    """
    combined_list = []
    for file in files:
        file.seek(0)  # Reset pointer for reliable re-reads across cache hits
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        combined_list.append(df)
    return pd.concat(combined_list, ignore_index=True)


def process_analytics(df: pd.DataFrame, sales_column: str) -> dict:
    """
    Cleans the target sales column and calculates core analytical metrics.
    """
    if sales_column not in df.columns:
        raise ValueError(f"Selected column '{sales_column}' does not exist in the dataset.")

    # Copy column to prevent altering original data view
    sales_series = df[sales_column].copy()

    # Clean data if it comes in as string/currency format
    if sales_series.dtype == 'object':
        sales_series = (
            sales_series.astype(str)
                .str.replace(r'[$,\s]', '', regex=True)
        )

    # Convert safely to numeric values, changing errors to NaN
    numeric_sales = pd.to_numeric(sales_series, errors='coerce')

    # Drop missing rows to ensure valid mathematical output
    clean_sales = numeric_sales.dropna()

    if clean_sales.empty:
        raise ValueError(f"No valid numeric data found in column '{sales_column}'.")

    return {
        "total_sales": float(clean_sales.sum()),
        "average_sales": float(clean_sales.mean()),
        "transaction_count": int(clean_sales.count())
    }
