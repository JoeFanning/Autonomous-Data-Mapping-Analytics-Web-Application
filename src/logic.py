import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def merge_and_load_spreadsheets(files) -> pd.DataFrame:
    """Safely loads and merges multiple uploaded Excel or CSV files."""
    all_dataframes = []

    for file in files:
        file_name = file.name.lower()
        try:
            if file_name.endswith('.csv') or file_name.endswith('.txt'):
                df = pd.read_csv(file)
            elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                df = pd.read_excel(file)
            else:
                continue

            all_dataframes.append(df)

        except Exception as e:
            continue

    if not all_dataframes:
        return pd.DataFrame()

    return pd.concat(all_dataframes, ignore_index=True)


def target_price_column_only(numeric_columns):
    """Identifies the best matching price column string using semantic similarity.

    Replaced CountVectorizer/Naive Bayes with the all-MiniLM-L6-v2 transformer.
    """
    if not numeric_columns:
        return None

    # Core anchor concepts used to measure semantic overlap
    reference_concepts = [
        "total price", "line total", "extended price", "total amount",
        "grand total", "total cost", "final price", "invoice total",
        "net total", "gross total", "total due", "amount due", "subtotal"
    ]

    # Initialize the lightweight semantic embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Compute embedded vectors for your ideal target concepts
    reference_embeddings = model.encode(reference_concepts)

    # Clean and flatten incoming list configurations
    numeric_columns = list(numeric_columns)
    if len(numeric_columns) == 1 and isinstance(numeric_columns[0], (list, tuple)):
        numeric_columns = list(numeric_columns[0])

    if not numeric_columns:
        print("No numeric columns provided to test.")
        return None

    # Compute embedded vectors for all current table columns
    column_strings = [str(col) for col in numeric_columns]
    column_embeddings = model.encode(column_strings)

    # Calculate cosine similarity matrix between columns and target concepts
    similarity_matrix = cosine_similarity(column_embeddings, reference_embeddings)

    # Take the highest matching score across any reference concept for each column
    max_scores = np.max(similarity_matrix, axis=1)

    # Extract the absolute best candidate index
    best_index = np.argmax(max_scores)
    candidate_column = numeric_columns[best_index]
    candidate_score = max_scores[best_index]

    col_clean = str(candidate_column).lower()
    strict_threshold = 0.50  # Sentence-Transformers use a lower, tighter baseline than Naive Bayes

    # Hard Shield veto rules
    if any(veto in col_clean for veto in ["average", "avg", "median", "unit", "qty", "quantity"]):
        print(f"Best column '{candidate_column}' was vetoed by the hard shield rule.")
        return None

    # Strict confidence validation check
    if candidate_score > strict_threshold:
        print(f"Successfully selected single best winner: '{candidate_column}' ({candidate_score:.2%} semantic match)")
        return candidate_column
    else:
        print(f"Best column '{candidate_column}' dropped. Score ({candidate_score:.2%}) was below threshold.")
        return None


def process_analytics(df: pd.DataFrame, column: str) -> dict:
    """Calculates granular pricing analytics data into a clean dictionary."""
    if isinstance(column, list):
        if len(column) > 0:
            column = column[0]
        else:
            column = df.columns[0]

    numeric_series = pd.to_numeric(df[column], errors='coerce').dropna()

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
