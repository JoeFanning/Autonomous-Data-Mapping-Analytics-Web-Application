import pandas as pd

def process_and_combine_files(uploaded_files):
    """Combines multiple files and runs basic statistical analysis."""
    all_dataframes = []
    
    for file in uploaded_files:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        all_dataframes.append(df)
    
    # Merge everything together
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    
    # Generate analytics metrics
    metrics = {
        "total_files": len(uploaded_files),
        "total_rows": len(combined_df),
        "total_columns": len(combined_df.columns),
        "summary_stats": combined_df.describe().to_string()
    }
    
    return metrics

