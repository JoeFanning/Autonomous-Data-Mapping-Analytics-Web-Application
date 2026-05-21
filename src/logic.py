import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def merge_and_load_spreadsheets(files) -> pd.DataFrame:
    """Parses raw files and merges them into a single dataframe."""
    combined_list = []
    for file in files:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        df.columns = df.columns.str.strip()
        combined_list.append(df)
    return pd.concat(combined_list, ignore_index=True) if combined_list else pd.DataFrame()


def target_price_column_only(numeric_columns):
    """Uses a Naive Bayes Machine Learning model to identify the matching price column string."""
    if not numeric_columns:
        return None

    price_keywords = [
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

    non_price_keywords = [
        "id", "customer_id", "order_id", "quantity", "qty", "count", "amount",
        "year", "month", "day", "date", "zip", "phone", "weight", "height",
        "width", "index", "serial", "age", "latitude", "longitude", "score",

        "ID", "CUSTOMER_ID", "ORDER_ID", "QUANTITY", "QTY", "COUNT", "AMOUNT",
        "YEAR", "MONTH", "DAY", "DATE", "ZIP", "PHONE", "WEIGHT", "HEIGHT",
        "WIDTH", "INDEX", "SERIAL", "AGE", "LATITUDE", "LONGITUDE", "SCORE",

        "Id", "Customer_id", "Order_id", "Quantity", "Qty", "Count", "Amount",
        "Year", "Month", "Day", "Date", "Zip", "Phone", "Weight", "Height",
        "Width", "Index", "Serial", "Age", "Latitude", "Longitude", "Score"
    ]

    X_train_text = price_keywords + non_price_keywords
    y_train = [1] * len(price_keywords) + [0] * len(non_price_keywords)

    vectorizer = CountVectorizer(lowercase=False)
    X_train_vectors = vectorizer.fit_transform(X_train_text)

    clf = MultinomialNB()
    clf.fit(X_train_vectors, y_train)

    X_test_vectors = vectorizer.transform(numeric_columns)
    probabilities = clf.predict_proba(X_test_vectors)[:, 1]

    best_match_idx = np.argmax(probabilities)
    if probabilities[best_match_idx] > 0.5:
        return numeric_columns[best_match_idx]
    return None


def process_analytics(df: pd.DataFrame, column: str) -> dict:
    """Calculates granular pricing analytics data into a clean dictionary."""

    # drops any non numeric cells in that 'price' column doesn't drop the whole row
    clean_series = df[column].dropna()

    # acts as a safety guard clause to prevent your code from crashing when there is no data to analyze
    if clean_series.empty:
        return {
            "total_revenue": 0.0,
            "highest_price": 0.0,
            "lowest_price": 0.0,
            "average_price": 0.0,
            "median": 0.0,
            "standard_deviation": 0.0,
            "transaction_count": 0
        }

    return {
        "total_revenue": float(clean_series.sum()),
        "highest_price": float(clean_series.max()),
        "lowest_price": float(clean_series.min()),
        "average_price": float(clean_series.mean()),
        "median": float(clean_series.median()),
        "standard_deviation": float(clean_series.std()) if len(clean_series) > 1 else 0.0,
        "transaction_count": int(clean_series.count())

    }


def calculate_text_distribution(df, column):
    """Isolates, cleans, and structures string count maps."""
    counts = df[column].astype(str).str.strip().value_counts().reset_index()
    counts.columns = ["Element Name", "Total Occurrences"]
    return counts
