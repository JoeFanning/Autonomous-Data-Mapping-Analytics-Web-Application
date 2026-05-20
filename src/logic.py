import pandas as pd
import streamlit as st


@st.cache_data(show_spinner="Combining **Excel** and **CSV** files...")
def merge_and_load_spreadsheets(files) -> pd.DataFrame:
    """
    Parses files and merges them completely, keeping all raw data types.
    """
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
                st.subheader("Column Totals & Averages")
                selected_num_col = st.selectbox(
                    "Select a numeric column:", numeric_cols
                )

                # Calculate calculations safely dropping null values
                clean_series = df[selected_num_col].dropna()

                if not clean_series.empty:
                    total_val = float(clean_series.sum())
                    avg_val = float(clean_series.mean())

                    # Display metrics side-by-side
                    m_col1, m_col2 = st.columns(2)
                    m_col1.metric(
                        label=f"Total of {selected_num_col}",
                        value=f"{total_val:,.2f}",
                    )
                    m_col2.metric(
                        label=f"Average of {selected_num_col}",
                        value=f"{avg_val:,.2f}",
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
                # This turns [door, door, window] into a clean counted list
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
    """
    Calculates total sales, average sales, and transaction counts
    for a chosen numeric column. Safely handles missing data.
    """
    # Exclude null/missing entries for clean calculations
    clean_series = df[column].dropna()

    if clean_series.empty:
        return {
            "total_sales": 0.0,
            "average_sales": 0.0,
            "transaction_count": 0
        }

    return {
        "total_sales": float(clean_series.sum()),
        "average_sales": float(clean_series.mean()),
        "transaction_count": int(clean_series.count())
    }
