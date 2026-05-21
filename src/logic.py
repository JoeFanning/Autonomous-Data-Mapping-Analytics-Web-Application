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
        # Lowercase
        "total price", "linetotal", "extended price", "extended_price", "total amount", "grand total", "line_total",
        "ext_price", "ext.price", "line.total", "total_prc", "t_prc", "tot_prc", "t_amount", "t.amount",
        "total_cost", "t_cost", "t.cost", "final price", "final_price",
        "order total", "order_total", "invoice total", "invoice_total",
        "net total", "net_total", "gross total", "gross_total", "total due", "total_due",
        "amount due", "amount_due", "charge total", "charge_total",
        "total summary", "total_summary", "full price", "full_price",
        "subtotal", "sub_total", "sub.total", "row total", "row_total",
        "item total", "item_total", "total cost", "total_cost", "net amount", "net_amount",
        "gross amount", "gross_amount", "total charge", "total_charge", "charged amount", "charged_amount",
        "total value", "total_value", "value", "final value", "final_value",
        "precio total", "total precio", "prix total", "total prix",
        "gesamtpreis", "endpreis", "summe",

        # UPPERCASE
        "TOTAL PRICE", "LINETOTAL", "EXTENDED PRICE", "EXTENDED_PRICE", "TOTAL AMOUNT", "GRAND TOTAL", "LINE_TOTAL",
        "EXT_PRICE", "EXT.PRICE", "LINE.TOTAL", "TOTAL_PRC", "T_PRC", "TOT_PRC", "T_AMOUNT", "T.AMOUNT",
        "TOTAL_COST", "T_COST", "T.COST", "FINAL PRICE", "FINAL_PRICE",
        "ORDER TOTAL", "ORDER_TOTAL", "INVOICE TOTAL", "INVOICE_TOTAL",
        "NET TOTAL", "NET_TOTAL", "GROSS TOTAL", "GROSS_TOTAL", "TOTAL DUE", "TOTAL_DUE",
        "AMOUNT DUE", "AMOUNT_DUE", "CHARGE TOTAL", "CHARGE_TOTAL",
        "TOTAL SUMMARY", "TOTAL_SUMMARY", "FULL PRICE", "FULL_PRICE",
        "SUBTOTAL", "SUB_TOTAL", "SUB.TOTAL", "ROW TOTAL", "ROW_TOTAL",
        "ITEM TOTAL", "ITEM_TOTAL", "TOTAL COST", "TOTAL_COST", "NET AMOUNT", "NET_AMOUNT",
        "GROSS AMOUNT", "GROSS_AMOUNT", "TOTAL CHARGE", "TOTAL_CHARGE", "CHARGED AMOUNT", "CHARGED_AMOUNT",
        "TOTAL VALUE", "TOTAL_VALUE", "VALUE", "FINAL VALUE", "FINAL_VALUE",
        "PRECIO TOTAL", "TOTAL PRECIO", "PRIX TOTAL", "TOTAL PRIX",
        "GESAMTPREIS", "ENDPREIS", "SUMME",

        # Title Case
        "Total Price", "Linetotal", "Extended Price", "Extended_price", "Total Amount", "Grand Total", "Line_total",
        "Ext_price", "Ext.price", "Line.total", "Total_prc", "T_prc", "Tot_prc", "T_amount", "T.amount",
        "Total_cost", "T_cost", "T.cost", "Final Price", "Final_price",
        "Order Total", "Order_total", "Invoice Total", "Invoice_total",
        "Net Total", "Net_total", "Gross Total", "Gross_total", "Total Due", "Total_due",
        "Amount Due", "Amount_due", "Charge Total", "Charge_total",
        "Total Summary", "Total_summary", "Full Price", "Full_price",
        "Subtotal", "Sub_total", "Sub.total", "Row Total", "Row_total",
        "Item Total", "Item_total", "Net Amount", "Net_amount", "Gross Amount", "Gross_amount",
        "Total Charge", "Total_charge", "Charged Amount", "Charged_amount",
        "Total Value", "Total_value", "Value", "Final Value", "Final_value",
        "Precio Total", "Total Precio", "Prix Total", "Total Prix",
        "Gesamtpreis", "Endpreis", "Summe"
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

    # If 'column' was passed as a list (e.g., ['Total Price']), grab the first item string
    if isinstance(column, list):
        if len(column) > 0:
            column = column[0]
        else:
            # Handle edge case where the list is completely empty
            column = df.columns[0]

    # Now df[column] is guaranteed to be a 1-D Series, preventing the TypeError
    numeric_series = pd.to_numeric(df[column], errors='coerce').dropna()

    # (Keep the rest of your guard clause and return block exactly the same)
    if numeric_series.empty:
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
        "total_revenue": float(numeric_series.sum()),
        "highest_price": float(numeric_series.max()),
        "lowest_price": float(numeric_series.min()),
        "average_price": float(numeric_series.mean()),
        "median": float(numeric_series.median()),
        "standard_deviation": float(numeric_series.std()) if len(numeric_series) > 1 else 0.0,
        "transaction_count": int(numeric_series.count())
    }


def calculate_text_distribution(df, column):
    """Isolates, cleans, and structures string count maps."""
    counts = df[column].astype(str).str.strip().value_counts().reset_index()
    counts.columns = ["Element Name", "Total Occurrences"]
    return counts
