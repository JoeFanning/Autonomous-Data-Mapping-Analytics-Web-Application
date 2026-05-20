import resend
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def target_price_column_only(numeric_columns):
    """Uses a Naive Bayes Machine Learning model trained on explicitly provided

    lowercase, uppercase, and title-case variations to identify price columns.
    """
    if not numeric_columns:
        return None

    # 1. EXPLICIT PRICE KEYWORDS: ALL LOWERCASE, ALL UPPERCASE, AND TITLE CASE
    price_keywords = [
        # --- Lowercase ---
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
        "preis", "stückpreis", "stueckpreis",

        # --- UPPERCASE ---
        "PRICE", "UNITPRICE", "RATE", "UNITRATE", "COST", "UNITCOST", "U_PRICE",
        "U.PRICE", "UN.PRICE", "UNIT_PRC", "U_PRC", "PRC", "U_RATE", "U.RATE",
        "UCOST", "U_COST", "U.COST", "VARIANT PRICE", "VARIANT_PRICE",
        "REGULAR PRICE", "REGULAR_PRICE", "SALE PRICE", "SALE_PRICE",
        "RETAIL PRICE", "RETAIL_PRICE", "MSRP", "LIST PRICE", "LIST_PRICE",
        "SELL PRICE", "SELLING PRICE", "WHOLESALE PRICE", "WHOLESALE_PRICE",
        "PURCHASE PRICE", "PURCHASE_PRICE", "SUPPLY COST", "SUPPLY_PRICE",
        "BASE PRICE", "BASE_PRICE", "DEFAULT PRICE", "DEFAULT_PRICE",
        "AMOUNT PER UNIT", "AMOUNT_PER_UNIT", "ITEM PRICE", "ITEM_PRICE",
        "ITEM COST", "ITEM_COST", "NET PRICE", "NET_PRICE", "GROSS PRICE",
        "GROSS_PRICE", "PRICE EACH", "PRICE_EACH", "PRICE/EACH", "CHARGE AMOUNT",
        "CHARGE_AMOUNT", "UNIT_AMOUNT", "UNIT AMOUNT", "VALUE", "UNIT VALUE",
        "UNIT_VALUE", "PRECIO", "PRECIO UNITARIO", "PRIX", "PRIX UNITAIRE",
        "PREIS", "STÜCKPREIS", "STUECKPREIS",

        # --- Title Case ---
        "Price", "Unitprice", "Rate", "Unitrate", "Cost", "Unitcost", "U_price",
        "U.price", "Un.price", "Unit_prc", "U_prc", "Prc", "U_rate", "U.rate",
        "Ucost", "U_cost", "U.cost", "Variant Price", "Variant_price",
        "Regular Price", "Regular_price", "Sale Price", "Sale_price",
        "Retail Price", "Retail_price", "Msrp", "List Price", "List_price",
        "Sell Price", "Selling Price", "Wholesale Price", "Wholesale_price",
        "Purchase Price", "Purchase_price", "Supply Cost", "Supply_price",
        "Base Price", "Base_price", "Default Price", "Default_price",
        "Amount Per Unit", "Amount_per_unit", "Item Price", "Item_price",
        "Item Cost", "Item_cost", "Net Price", "Net_price", "Gross Price",
        "Gross_price", "Price Each", "Price_each", "Price/each", "Charge Amount",
        "Charge_amount", "Unit_amount", "Unit Amount", "Value", "Unit Value",
        "Unit_value", "Precio", "Precio Unitario", "Prix", "Prix Unitaire",
        "Preis", "Stückpreis", "Stueckpreis"
    ]

    # 2. EXPLICIT NON-PRICE KEYWORDS: ALL LOWERCASE, ALL UPPERCASE, AND TITLE CASE
    non_price_keywords = [
        # --- Lowercase ---
        "id", "customer_id", "order_id", "quantity", "qty", "count", "amount",
        "year", "month", "day", "date", "zip", "phone", "weight", "height",
        "width", "index", "serial", "age", "latitude", "longitude", "score",

        # --- UPPERCASE ---
        "ID", "CUSTOMER_ID", "ORDER_ID", "QUANTITY", "QTY", "COUNT", "AMOUNT",
        "YEAR", "MONTH", "DAY", "DATE", "ZIP", "PHONE", "WEIGHT", "HEIGHT",
        "WIDTH", "INDEX", "SERIAL", "AGE", "LATITUDE", "LONGITUDE", "SCORE",

        # --- Title Case ---
        "Id", "Customer_id", "Order_id", "Quantity", "Qty", "Count", "Amount",
        "Year", "Month", "Day", "Date", "Zip", "Phone", "Weight", "Height",
        "Width", "Index", "Serial", "Age", "Latitude", "Longitude", "Score"
    ]

    # Combine into a single training dataset
    X_train_text = price_keywords + non_price_keywords

    # Target labels: 1 for Price, 0 for Non-Price
    # Target labels: [1] multiplied by how many price words, plus [0] multiplied by how many non-price words
    y_train = [1] * len(price_keywords) + [0] * len(non_price_keywords)

    # VECTORIZATION: Turn text into numbers.
    # lowercase=False forces the model to respect your case variations explicitly.
    vectorizer = CountVectorizer(lowercase=False)
    X_train_vectors = vectorizer.fit_transform(X_train_text)

    # TRAIN THE MODEL
    clf = MultinomialNB()
    clf.fit(X_train_vectors, y_train)

    # PREDICTION
    X_test_vectors = vectorizer.transform(numeric_columns)
    probabilities = clf.predict_proba(X_test_vectors)[:, 1]

    # Find the best match
    best_match_idx = np.argmax(probabilities)
    highest_probability = probabilities[best_match_idx]

    # Confidence Threshold (Must be more than 50% sure)
    if highest_probability > 0.5:
        return numeric_columns[best_match_idx]

    return None


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

        # 1. EXCLUSIVE PRICE METRICS
        if numeric_cols:
            detected_price_col = target_price_column_only(numeric_cols)

            if detected_price_col:
                st.subheader(f"📊 Auto-Detected Price Metrics (`{detected_price_col}`)")

                clean_series = df[detected_price_col].dropna()

                if not clean_series.empty:
                    highest_val = float(clean_series.max())
                    lowest_val = float(clean_series.min())
                    avg_val = float(clean_series.mean())
                    std_val = float(clean_series.std()) if len(clean_series) > 1 else 0.0

                    median_val = float(clean_series.median())
                    range_spread = highest_val - lowest_val
                    total_sum = float(clean_series.sum())
                    record_count = int(clean_series.count())

                    row1_col1, row1_col2 = st.columns(2)
                    row2_col1, row2_col2 = st.columns(2)
                    row3_col1, row3_col2 = st.columns(2)
                    row4_col1, row4_col2 = st.columns(2)

                    row1_col1.metric(label="Highest Price Found", value=f"${highest_val:,.2f}")
                    row1_col2.metric(label="Lowest Price Found", value=f"${lowest_val:,.2f}")

                    row2_col1.metric(label="Average Price (Mean)", value=f"${avg_val:,.2f}")
                    row2_col2.metric(label="Median Price (Middle Point)", value=f"${median_val:,.2f}")

                    row3_col1.metric(label="Price Range Spread", value=f"${range_spread:,.2f}")
                    row3_col2.metric(label="Standard Deviation", value=f"{std_val:,.2f}")

                    row4_col1.metric(label="Total Volumetric Sum", value=f"${total_sum:,.2f}")
                    row4_col2.metric(label="Total Record Count", value=f"{record_count:,}")
                else:
                    st.warning(f"The column '{detected_price_col}' contains no valid numbers.")
            else:
                st.error("❌ Could not automatically find a price or unit price column in this file.")
                st.info("Ensure your file has a column header like: Price, Unit Price, Cost, Rate, or MSRP.")
        else:
            st.info("No numeric columns found in this dataset.")

    elif df is not None and df.empty:
        st.warning("Uploaded files do not contain usable data.")

    return email, files, submit_button
