import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def merge_and_load_spreadsheets(files) -> pd.DataFrame:
    """Safely loads and merges multiple uploaded Excel or CSV files."""
    all_dataframes = []

    for file in files:
        # Grab the file name to inspect its extension
        file_name = file.name.lower()

        try:
            if file_name.endswith('.csv') or file_name.endswith('.txt'):
                # Read CSV or flat text data layout files safely
                df = pd.read_csv(file)
            elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                # Read standard Excel sheets safely
                df = pd.read_excel(file)
            else:
                continue

            all_dataframes.append(df)

        except Exception as e:
            # Prevent a corrupted single file from crashing the entire user session
            continue

    if not all_dataframes:
        return pd.DataFrame()  # Return clean empty dataframe to trigger your guard clauses

    # Combine all individual tables matching layout fields
    return pd.concat(all_dataframes, ignore_index=True)


def target_price_column_only(numeric_columns):
    """Uses a Naive Bayes Machine Learning model to identify the matching price column string."""
    if not numeric_columns:
        return None
    price_keywords = [
        # Lowercase
        "total price", "total_price", "total-price", "totalprice",
        "line total", "line_total", "line-total", "linetotal", "line.total",
        "extended price", "extended_price", "extended-price", "extendedprice",
        "ext price", "ext_price", "ext-price", "extprice", "ext.price",
        "total amount", "total_amount", "total-amount", "totalamount",
        "t amount", "t_amount", "t-amount", "tamount", "t.amount",
        "grand total", "grand_total", "grand-total", "grandtotal",
        "total prc", "total_prc", "total-prc", "totalprc",
        "t prc", "t_prc", "t-prc", "tprc",
        "tot prc", "tot_prc", "tot-prc", "totprc",
        "total cost", "total_cost", "total-cost", "totalcost",
        "t cost", "t_cost", "t-cost", "tcost", "t.cost",
        "final price", "final_price", "final-price", "finalprice",
        "order total", "order_total", "order-total", "ordertotal",
        "invoice total", "invoice_total", "invoice-total", "invoicetotal",
        "net total", "net_total", "net-total", "nettotal",
        "gross total", "gross_total", "gross-total", "grosstotal",
        "total due", "total_due", "total-due", "totaldue",
        "amount due", "amount_due", "amount-due", "amountdue",
        "charge total", "charge_total", "charge-total", "chargetotal",
        "total summary", "total_summary", "total-summary", "totalsummary",
        "full price", "full_price", "full-price", "fullprice",
        "subtotal", "sub_total", "sub-total", "sub.total",
        "row total", "row_total", "row-total", "rowtotal",
        "item total", "item_total", "item-total", "itemtotal",
        "net amount", "net_amount", "net-amount", "netamount",
        "gross amount", "gross_amount", "gross-amount", "grossamount",
        "total charge", "total_charge", "total-charge", "totalcharge",
        "charged amount", "charged_amount", "charged-amount", "chargedamount",
        "total value", "total_value", "total-value", "totalvalue",
        "final value", "final_value", "final-value", "finalvalue",
        "value", "precio total", "total precio", "prix total", "total prix",
        "gesamtpreis", "endpreis", "summe",

        # UPPERCASE
        "TOTAL PRICE", "TOTAL_PRICE", "TOTAL-PRICE", "TOTALPRICE",
        "LINE TOTAL", "LINE_TOTAL", "LINE-TOTAL", "LINETOTAL", "LINE.TOTAL",
        "EXTENDED PRICE", "EXTENDED_PRICE", "EXTENDED-PRICE", "EXTENDEDPRICE",
        "EXT PRICE", "EXT_PRICE", "EXT-PRICE", "EXTPRICE", "EXT.PRICE",
        "TOTAL AMOUNT", "TOTAL_AMOUNT", "TOTAL-AMOUNT", "TOTALAMOUNT",
        "T AMOUNT", "T_AMOUNT", "T-AMOUNT", "TAMOUNT", "T.AMOUNT",
        "GRAND TOTAL", "GRAND_TOTAL", "GRAND-TOTAL", "GRANDTOTAL",
        "TOTAL PRC", "TOTAL_PRC", "TOTAL-PRC", "TOTALPRC",
        "T PRC", "T_PRC", "T-PRC", "TPRC",
        "TOT PRC", "TOT_PRC", "TOT-PRC", "TOTPRC",
        "TOTAL COST", "TOTAL_COST", "TOTAL-COST", "TOTALCOST",
        "T COST", "T_COST", "T-COST", "TCOST", "T.COST",
        "FINAL PRICE", "FINAL_PRICE", "FINAL-PRICE", "FINALPRICE",
        "ORDER TOTAL", "ORDER_TOTAL", "ORDER-TOTAL", "ORDERTOTAL",
        "INVOICE TOTAL", "INVOICE_TOTAL", "INVOICE-TOTAL", "INVOICETOTAL",
        "NET TOTAL", "NET_TOTAL", "NET-TOTAL", "NETTOTAL",
        "GROSS TOTAL", "GROSS_TOTAL", "GROSS-TOTAL", "GROSSTOTAL",
        "TOTAL DUE", "TOTAL_DUE", "TOTAL-DUE", "TOTALDUE",
        "AMOUNT DUE", "AMOUNT_DUE", "AMOUNT-DUE", "AMOUNTDUE",
        "CHARGE TOTAL", "CHARGE_TOTAL", "CHARGE-TOTAL", "CHARGETOTAL",
        "TOTAL SUMMARY", "TOTAL_SUMMARY", "TOTAL-SUMMARY", "TOTALSUMMARY",
        "FULL PRICE", "FULL_PRICE", "FULL-PRICE", "FULLPRICE",
        "SUBTOTAL", "SUB_TOTAL", "SUB-TOTAL", "SUB.TOTAL",
        "ROW TOTAL", "ROW_TOTAL", "ROW-TOTAL", "ROWTOTAL",
        "ITEM TOTAL", "ITEM_TOTAL", "ITEM-TOTAL", "ITEMTOTAL",
        "NET AMOUNT", "NET_AMOUNT", "NET-AMOUNT", "NETAMOUNT",
        "GROSS AMOUNT", "GROSS_AMOUNT", "GROSS-AMOUNT", "GROSSAMOUNT",
        "TOTAL CHARGE", "TOTAL_CHARGE", "TOTAL-CHARGE", "TOTALCHARGE",
        "CHARGED AMOUNT", "CHARGED_AMOUNT", "CHARGED-AMOUNT", "CHARGEDAMOUNT",
        "TOTAL VALUE", "TOTAL_VALUE", "TOTAL-VALUE", "TOTALVALUE",
        "FINAL VALUE", "FINAL_VALUE", "FINAL-VALUE", "FINALVALUE",
        "VALUE", "PRECIO TOTAL", "TOTAL PRECIO", "PRIX TOTAL", "TOTAL PRIX",
        "GESAMTPREIS", "ENDPREIS", "SUMME",

        # Title Case / CamelCase
        "Total Price", "Total_Price", "Total-Price", "TotalPrice",
        "Line Total", "Line_Total", "Line-Total", "LineTotal", "Line.Total",
        "Extended Price", "Extended_Price", "Extended-Price", "ExtendedPrice",
        "Ext Price", "Ext_Price", "Ext-Price", "ExtPrice", "Ext.Price",
        "Total Amount", "Total_Amount", "Total-Amount", "TotalAmount",
        "T Amount", "T_Amount", "T-Amount", "TAmount", "T.Amount",
        "Grand Total", "Grand_Total", "Grand-Total", "GrandTotal",
        "Total Prc", "Total_Prc", "Total-Prc", "TotalPrc",
        "T Prc", "T_Prc", "T-Prc", "TPrc",
        "Tot Prc", "Tot_Prc", "Tot-Prc", "TotPrc",
        "Total Cost", "Total_Cost", "Total-Cost", "TotalCost",
        "T Cost", "T_Cost", "T-Cost", "TCost", "T.Cost",
        "Final Price", "Final_Price", "Final-Price", "FinalPrice",
        "Order Total", "Order_Total", "Order-Total", "OrderTotal",
        "Invoice Total", "Invoice_Total", "Invoice-Total", "InvoiceTotal",
        "Net Total", "Net_Total", "Net-Total", "NetTotal",
        "Gross Total", "Gross_Total", "Gross-Total", "GrossTotal",
        "Total Due", "Total_due", "Total_Due", "Total-Due", "TotalDue",
        "Amount Due", "Amount_due", "Amount_Due", "Amount-Due", "AmountDue",
        "Charge Total", "Charge_total", "Charge_Due", "Charge_Total", "Charge-Total", "ChargeTotal",
        "Total Summary", "Total_summary", "Total_Summary", "Total-Summary", "TotalSummary",
        "Full Price", "Full_price", "Full_Price", "Full-Price", "FullPrice",
        "Subtotal", "Sub_total", "Sub_Total", "Sub-Total", "Sub.Total",
        "Row Total", "Row_total", "Row_Total", "Row-Total", "RowTotal",
        "Item Total", "Item_total", "Item_Total", "Item-Total", "ItemTotal",
        "Net Amount", "Net_amount", "Net_Amount", "Net-Amount", "NetAmount",
        "Gross Amount", "Gross_amount", "Gross_Amount", "Gross-Amount", "GrossAmount",
        "Total Charge", "Total_charge", "Total_Charge", "Total-Charge", "TotalCharge",
        "Charged Amount", "Charged_amount", "Charged_Amount", "Charged-Amount", "ChargedAmount",
        "Total Value", "Total_value", "Total_Value", "Total-Value", "TotalValue",
        "Final Value", "Final_value", "Final_Value", "Final-Value", "FinalValue",
        "Value", "Precio Total", "Total Precio", "Prix Total", "Total Prix",
        "Gesamtpreis", "Endpreis", "Summe"
    ]

    non_price_keywords = [
        # Lowercase
        "average",
        "unit price", "unit_price", "unit-price", "unitprice",
        "customer id", "customer_id", "customer-id", "customerid",
        "order id", "order_id", "order-id", "orderid",
        "id", "quantity", "qty", "count", "amount", "year", "month", "day", "date", "zip",
        "phone", "weight", "height", "width", "index", "serial", "age", "latitude", "longitude", "score",

        # UPPERCASE
        "AVERAGE",
        "UNIT PRICE", "UNIT_PRICE", "UNIT-PRICE", "UNITPRICE",
        "CUSTOMER ID", "CUSTOMER_ID", "CUSTOMER-ID", "CUSTOMERID",
        "ORDER ID", "ORDER_ID", "ORDER-ID", "ORDERID",
        "ID", "QUANTITY", "QTY", "COUNT", "AMOUNT", "YEAR", "MONTH", "DAY", "DATE", "ZIP",
        "PHONE", "WEIGHT", "HEIGHT", "WIDTH", "INDEX", "SERIAL", "AGE", "LATITUDE", "LONGITUDE", "SCORE",

        # Title Case / CamelCase
        "Average"
        "Unit Price", "Unit_Price", "Unit-Price", "UnitPrice", "Unitprice",
        "Customer Id", "Customer_Id", "Customer-Id", "CustomerId", "Customer_id",
        "Order Id", "Order_Id", "Order-Id", "OrderId", "Order_id",
        "Id", "Quantity", "Qty", "Count", "Amount", "Year", "Month", "Day", "Date", "Zip",
        "Phone", "Weight", "Height", "Width", "Index", "Serial", "Age", "Latitude", "Longitude", "Score"
    ]

    # Combine two lists together into one long list of text samples.
    X_train_text = price_keywords + non_price_keywords
    # Creates the matching target labels. It assigns a 1 (Total Price) to every item from price_keywords,
    # and a 0 (Not Total Price) to every item from non_price_keywords
    y_train = [1] * len(price_keywords) + [0] * len(non_price_keywords)

    # Use character slicing instead of whole words.
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 4), lowercase=False)
    X_train_vectors = vectorizer.fit_transform(X_train_text)

    # This initializes a Multinomial Naive Bayes classifier (clf) and trains it (.fit()).
    clf = MultinomialNB()
    clf.fit(X_train_vectors, y_train)

    # --- FIX 1: UNWRAP THE LIST IMMEDIATELY HERE ---
    numeric_columns = list(numeric_columns)
    if len(numeric_columns) == 1 and isinstance(numeric_columns[0], (list, tuple)):
        numeric_columns = list(numeric_columns[0])

    # 1. Calculate probabilities for ALL numeric columns at once (now beautifully flattened)
    X_test_vectors = vectorizer.transform(numeric_columns)
    probabilities = clf.predict_proba(X_test_vectors)[:, 1]

    # Initialize your output variable cleanly
    best_column = None
    strict_threshold = 0.80

    # 2. Extract ONLY the single absolute best candidate
    if len(numeric_columns) > 0:
        # Find the index position of the highest probability value
        best_index = np.argmax(probabilities)

        # Grab that candidate and its score
        candidate_column = numeric_columns[best_index]
        candidate_score = probabilities[best_index]

        col_clean = candidate_column.lower()

        # 3. Apply your HARD SHIELD veto to the winner
        if "average" in col_clean or "avg" in col_clean or "median" in col_clean:
            print(f"Best column '{candidate_column}' was vetoed by the hard shield.")
            best_column = None

        # 4. Apply your strict 80% threshold to the winner
        elif candidate_score > strict_threshold:
            best_column = candidate_column
            print(f"Successfully selected single best winner: '{best_column}' ({candidate_score:.2%} confidence)")
        else:
            print(
                f"Best column '{candidate_column}' dropped because score ({candidate_score:.2%}) was below threshold.")
    else:
        print("No numeric columns provided to test.")

    # 5. Returns exactly one string header name, or None safely. No leaks!
    return best_column


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
