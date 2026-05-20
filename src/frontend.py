import re
import pandas as pd
import streamlit as st


def target_price_column_only(numeric_columns):
    """Scans numeric columns against known price keywords.

    Returns only the best matching price column name, or None if no match.
    """
    price_keywords = [
        "price",
        "unitprice",
        "rate",
        "unitrate",
        "cost",
        "unitcost",
        "u_price",
        "u.price",
        "un.price",
        "unit_prc",
        "u_prc",
        "prc",
        "u_rate",
        "u.rate",
        "ucost",
        "u_cost",
        "u.cost",
        "variant price",
        "variant_price",
        "regular price",
        "regular_price",
        "sale price",
        "sale_price",
        "retail price",
        "retail_price",
        "msrp",
        "list price",
        "list_price",
        "sell price",
        "selling price",
        "wholesale price",
        "wholesale_price",
        "purchase price",
        "purchase_price",
        "supply cost",
        "supply_price",
        "base price",
        "base_price",
        "default price",
        "default_price",
        "amount per unit",
        "amount_per_unit",
        "item price",
        "item_price",
        "item cost",
        "item_cost",
        "net price",
        "net_price",
        "gross price",
        "gross_price",
        "price each",
        "price_each",
        "price/each",
        "charge amount",
        "charge_amount",
        "unit_amount",
        "unit amount",
        "value",
        "unit value",
        "unit_value",
        "precio",
        "precio unitario",
        "prix",
        "prix unitaire",
        "preis",
        "stückpreis",
        "stueckpreis",
    ]

    best_match = None
    highest_score = 0

    for col in numeric_columns:
        sanitized = re.sub(r"[^a-z0-9]", "", col.lower())

        for kw in price_keywords:
            clean_kw = re.sub(r"[^a-z0-9]", "", kw.lower())

            # Perfect direct match
            if sanitized == clean_kw:
                return col

            # Fuzzy match (keyword contained inside the string)
            if clean_kw in sanitized:
                score = len(clean_kw)
                if score > highest_score:
                    highest_score = score
                    best_match = col

    return best_match


def render_ui(df: pd.DataFrame = None):
    """Renders the core website elements.

    Isolates data crunching exclusively to the detected price column.
    """
    st.title("📊 Enix Data Analytics")
    st.write(
        "Upload your **Excel(.xlsx)** or **CSV(.csv)** files. We will combine them, run analytics, and email you the report!"
    )

    # Input elements
    email = st.text_input(
        "📬 Enter your email address:", placeholder="your-email@example.com"
    )
    st.markdown("📁 Upload your spreadsheets (**CSV** or **Excel**):")

    files = st.file_uploader(
        label="Spreadsheet Upload Space",
        label_visibility="collapsed",
        type=["csv", "xlsx"],
        accept_multiple_files=True,
    )

    submit_button = st.button("🚀 Run Analytics & Email Report")

    # --- DYNAMIC FRONTEND DISPLAY BLOCK ---
    if df is not None and not df.empty:
        st.divider()

        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        text_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        tab1, tab2 = st.tabs(["🔢 Price Metrics", "🔤 Text Element Counter"])

        # --- TAB 1: EXCLUSIVE PRICE METRICS ---
        with tab1:
            if numeric_cols:
                # Find the single price column that matches your array of words
                detected_price_col = target_price_column_only(numeric_cols)

                if detected_price_col:
                    st.subheader(f"Price Metrics for: `{detected_price_col}`")

                    # Target only the isolated price column data
                    clean_series = df[detected_price_col].dropna()

                    if not clean_series.empty:
                        highest_val = float(clean_series.max())
                        lowest_val = float(clean_series.min())
                        avg_val = float(clean_series.mean())
                        std_val = (
                            float(clean_series.std())
                            if len(clean_series) > 1
                            else 0.0
                        )

                        # Grid UI layout display
                        row1_col1, row1_col2 = st.columns(2)
                        row2_col1, row2_col2 = st.columns(2)

                        row1_col1.metric(
                            label="Highest Price Found",
                            value=f"${highest_val:,.2f}",
                        )
                        row1_col2.metric(
                            label="Lowest Price Found", value=f"${lowest_val:,.2f}"
                        )
                        row2_col1.metric(
                            label="Average Price", value=f"${avg_val:,.2f}"
                        )
                        row2_col2.metric(
                            label="Standard Deviation", value=f"{std_val:,.2f}"
                        )
                    else:
                        st.warning(
                            f"The price column '{detected_price_col}' contains no valid numeric data."
                        )
                else:
                    st.error(
                        "❌ Could not automatically detect a price or unit price column in this spreadsheet."
                    )
                    st.info(
                        "Ensure your file has a column header like: Price, Unit Price, Cost, Rate, or MSRP."
                    )
            else:
                st.info("No numeric columns found in this dataset.")

        # --- TAB 2: TEXT ELEMENT COUNTER ---
        with tab2:
            if text_cols:
                st.subheader("Identical Element Counts")
                selected_text_col = st.selectbox(
                    "Select a text column to isolate elements:",
                    text_cols,
                    key="frontend_text_select",
                )

                counts = (
                    df[selected_text_col].astype(str).str.strip().value_counts()
                )
                counts_df = counts.reset_index()
                counts_df.columns = ["Element Name", "Total Occurrences"]

                st.dataframe(counts_df, use_container_width=True)
            else:
                st.info("No text columns found in this dataset.")

    elif df is not None and df.empty:
        st.warning("Uploaded files do not contain usable data.")

    return email, files, submit_button
