import re
import streamlit as st
import pandas as pd


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
        sanitized = re.sub(r'[^a-z0-9]', '', col.lower())
        if any(kw.replace(" ", "").replace("_", "").replace(".", "") in sanitized for kw in price_keywords):
            return index
    return 0


def render_ui(df: pd.DataFrame = None):
    """
    Renders the core website elements and explicitly handles the
    metric displays, tabs, and dataframes on the frontend.
    """
    st.title("📊 Enix Data Analytics")
    st.write(
        "Upload your **Excel(.xlsx)** or **CSV(.csv)** files. We will combine them, run analytics, and email you the report!")

    # Draw input spaces
    email = st.text_input("📬 Enter your email address:", placeholder="your-email@example.com")

    st.markdown("📁 Upload your spreadsheets (**CSV** or **Excel**):")

    files = st.file_uploader(
        label="Spreadsheet Upload Space",
        label_visibility="collapsed",
        type=["csv", "xlsx"],
        accept_multiple_files=True
    )

    submit_button = st.button("🚀 Run Analytics & Email Report")

    # --- DYNAMIC FRONTEND DISPLAY BLOCK ---
    # This renders the loaded data into the UI if a DataFrame exists
    if df is not None and not df.empty:
        st.divider()  # Visual break line

        # Split numeric and text columns
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        text_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        # Generate tabs directly inside the rendering lifecycle
        tab1, tab2 = st.tabs(["🔢 Numeric Metrics", "🔤 Text Element Counter"])

        # --- TAB 1: NUMERIC METRICS ---
        with tab1:
            if numeric_cols:
                st.subheader("Price Metrics Breakdown")

                default_idx = find_default_price_column(numeric_cols)
                selected_num_col = st.selectbox(
                    "Select a numeric column:",
                    numeric_cols,
                    index=default_idx,
                    key="frontend_num_select"
                )

                clean_series = df[selected_num_col].dropna()

                if not clean_series.empty:
                    highest_val = float(clean_series.max())
                    lowest_val = float(clean_series.min())
                    avg_val = float(clean_series.mean())
                    std_val = float(clean_series.std()) if len(clean_series) > 1 else 0.0

                    # 2x2 Grid Layout layout matching backend calculation
                    row1_col1, row1_col2 = st.columns(2)
                    row2_col1, row2_col2 = st.columns(2)

                    row1_col1.metric(label=f"Highest Price ({selected_num_col})", value=f"{highest_val:,.2f}")
                    row1_col2.metric(label=f"Lowest Price ({selected_num_col})", value=f"{lowest_val:,.2f}")
                    row2_col1.metric(label=f"Average Price ({selected_num_col})", value=f"{avg_val:,.2f}")
                    row2_col2.metric(label=f"Standard Deviation", value=f"{std_val:,.2f}")
                else:
                    st.warning("The selected column contains no numeric data.")
            else:
                st.info("No numeric columns found in this dataset.")

        # --- TAB 2: TEXT ELEMENT COUNTER ---
        with tab2:
            if text_cols:
                st.subheader("Identical Element Counts")
                selected_text_col = st.selectbox(
                    "Select a text column to isolate elements:",
                    text_cols,
                    key="frontend_text_select"
                )

                counts = df[selected_text_col].astype(str).str.strip().value_counts()
                counts_df = counts.reset_index()
                counts_df.columns = ["Element Name", "Total Occurrences"]

                st.dataframe(counts_df, use_container_width=True)
            else:
                st.info("No text columns found in this dataset.")

    elif df is not None and df.empty:
        st.warning("Uploaded files do not contain usable data.")

    return email, files, submit_button
