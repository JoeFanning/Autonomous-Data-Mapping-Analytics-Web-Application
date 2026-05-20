import re
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner="Combining **Excel** and **CSV** files...")
def merge_and_load_spreadsheets(files) -> pd.DataFrame:
    """Parses files and merges them completely, keeping all raw data types."""
    combined_list = []
    for file in files:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Strip spaces from column names to keep them consistent across files
        df.columns = df.columns.str.strip()
        combined_list.append(df)

    if not combined_list:
        return pd.DataFrame()

    return pd.concat(combined_list, ignore_index=True)


def find_default_price_column(numeric_columns):
    """Matches columns against known price keywords to find a default index."""
    price_keywords = {
        "price", "unitprice", "rate", "unitrate", "cost", "unitcost", "u_price",
        "u.price", "un.price", "unit_prc", "u_prc", "prc", "u_rate", "u.rate",
        "ucost", "u_cost", "u.cost", "variant price", "variant_price",
        "regular price", "regular_price", "sale price", "sale_price",
        "retail price", "retail_price", "msrp", "list price", "list_price",
        "sell price", "selling price", "wholesale price", "wholesale_price",
        "purchase price", "purchase_price", "supply cost", "supply_price",
        "base price", "base_price", "default price", "default_price",
        "amount per unit", "amount_per_unit", "item price", "item_price",
        "item cost", "item_cost", "net price", "net_price", "gross price",
        "gross_price", "price each", "price_each", "price/each", "charge amount",
        "charge_amount", "unit_amount", "unit amount", "value", "unit value",
        "unit_value", "precio", "precio unitario", "prix", "prix unitaire",
        "preis", "stückpreis", "stueckpreis"
    }

    for index, col in enumerate(numeric_columns):
        # Sanitize name by making lowercase and removing non-alphanumeric chars
        sanitized = re.sub(r'[^a-z0-9]', '', col.lower())

        # Check if the sanitized column name matches or contains any target words
        if any(kw.replace(" ", "").replace("_", "").replace(".", "") in sanitized for kw in price_keywords):
            return index

    return 0  # Fallback to the first column if no match is found


# --- UI Logic ---
st.title("Unified Data & Text Analyzer")

uploaded_files = st.file_uploader(
    "Upload files", type=["csv", "xlsx", "xls", "txt"], accept_multiple_files=True
)

if uploaded_files:
    # 1. Load the combined dataset
    df = merge_and_load_spreadsheets(uploaded_files)

    # 2. Reset file streams immediately after loading
    for f in uploaded_files:
        f.seek(0)

    if not df.empty:
        # Separate columns by data types
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        text_cols = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        # Create two structural tabs for clean navigation
        tab1, tab2 = st.tabs(["🔢 Numeric Metrics", "🔤 Text Element Counter"])

        # --- TAB 1: NUMERIC METRICS ---
        with tab1:
            if numeric_cols:
                st.subheader("Price Metrics Breakdown")

                # Automatically determine the best default column index
                default_idx = find_default_price_column(numeric_cols)

                selected_num_col = st.selectbox(
                    "Select a numeric column:",
                    numeric_cols,
                    index=default_idx
                )

                # Calculate calculations safely dropping null values
                clean_series = df[selected_num_col].dropna()

                if not clean_series.empty:
                    # Calculate required price analytics
                    highest_val = float(clean_series.max())
                    lowest_val = float(clean_series.min())
                    avg_val = float(clean_series.mean())
                    std_val = float(clean_series.std()) if len(clean_series) > 1 else 0.0

                    # Display metrics side-by-side in a 2x2 grid layout
                    row1_col1, row1_col2 = st.columns(2)
                    row2_col1, row2_col2 = st.columns(2)

                    row1_col1.metric(
                        label=f"Highest Price ({selected_num_col})",
                        value=f"{highest_val:,.2f}",
                    )
                    row1_col2.metric(
                        label=f"Lowest Price ({selected_num_col})",
                        value=f"{lowest_val:,.2f}",
                    )
                    row2_col1.metric(
                        label=f"Average Price ({selected_num_col})",
                        value=f"{avg_val:,.2f}",
                    )
                    row2_col2.metric(
                        label=f"Standard Deviation",
                        value=f"{std_val:,.2f}",
                    )
                else:
                    st.warning("The selected column contains no numeric data.")
            else:
                st.info("No numeric columns found in this dataset.")

        # --- TAB 2: TEXT ELEMENT COUNTER ---
        with tab2:
            if text_cols:
                st.subheader("Identical Element Counts")
                selected_text_col = st.selectbox(
                    "Select a text column to isolate elements:", text_cols
                )

                # Isolate, clean, and count identical string matches
                counts = (
                    df[selected_text_col]
                        .astype(str)
                        .str.strip()
                        .value_counts()
                )

                # Format counts into a clean dataframe for presentation
                counts_df = counts.reset_index()
                counts_df.columns = ["Element Name", "Total Occurrences"]

                # Display the isolated breakdown table
                st.dataframe(counts_df, use_container_width=True)
            else:
                st.info("No text columns found in this dataset.")
    else:
        st.warning("Uploaded files do not contain usable data.")


def process_analytics(df, column):
    clean_series = df[column].dropna()

    if clean_series.empty:
        return {
            "highest_price": 0.0, "lowest_price": 0.0, "average_price": 0.0, "standard_deviation": 0.0,
            "total_sales": 0.0, "transaction_count": 0, "median_price": 0.0, "price_range": 0.0,
            "q1_price": 0.0, "q3_price": 0.0
        }

    return {
        "highest_price": float(clean_series.max()),
        "lowest_price": float(clean_series.min()),
        "average_price": float(clean_series.mean()),
        "standard_deviation": float(clean_series.std()) if len(clean_series) > 1 else 0.0,
        "total_sales": float(clean_series.sum()),
        "transaction_count": int(clean_series.count()),
        "median_price": float(clean_series.median()),
        "price_range": float(clean_series.max() - clean_series.min()),
        "q1_price": float(clean_series.quantile(0.25)),
        "q3_price": float(clean_series.quantile(0.75))
    }
