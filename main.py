import streamlit as st
# Explicitly route imports into your 'src' directory structure
from src import frontend  # Owns the UI Look
from src import logic  # Owns the ML & Math Data Brain
from src import mailer  # Owns the Email Dispatch Delivery

# 1. Run the base web UI interface setup tools
uploaded_files, user_email, submit_clicked = frontend.render_base_uploader_ui()

if uploaded_files:

    # @st.cache_data: This is a Streamlit decorator. It saves (caches) the output of the function
    # in your computer's memory based on the input files.
    # show_spinner="...": This displays a temporary loading message and spinner on the user's screen
    # while the function runs for the first time.
    @st.cache_data(show_spinner="Combining and loading dataset structures...")
    #  This defines the helper function that accepts a list of raw files.
    def process_raw_files(files):
        # A Streamlit function. This calls an external custom script (logic) to
        # combine and format the spreadsheets into a unified dataset.
        return logic.merge_and_load_spreadsheets(files)

    # This line of code executes the caching function and stores the final, combined dataset into
    # a pandas DataFrame named df
    df = process_raw_files(uploaded_files)

    #File Reading Concept: Python treats uploaded files like a VHS tape or a physical book. When a
    # function (like your process_raw_files) reads a file, it moves an internal cursor from the beginning to the end.
    # The "Empty File" Trap: If you try to read the file a second time without resetting it, Python starts reading from
    # the very end of the file. This results in an empty string or an empty DataFrame, often causing silent bugs or crashes.
    # f.seek(0): This forces the cursor back to the start line. It allows you to safely re-read, validate, or process the
    # same uploaded files multiple times within your app.
    for f in uploaded_files:
        f.seek(0)
    # if not df.empty:: This acts as a safety guard. It ensures the DataFrame actually contains rows and columns before
    # trying to analyze it, preventing errors if the uploaded files were blank.
    if not df.empty:
        # df.select_dtypes(...): This is a pandas method that filters your DataFrame columns by their data types
        # include=["number"]: This targets all numeric columns, including integers (int64) and floats (float64).
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        # include=["object", "category"]: This targets text columns (strings are stored as object in pandas) and categorical columns.
        # .columns.tolist(): This extracts just the names of those filtered columns and converts them into a clean Python list.
        text_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        # Route numeric attributes downstream into backend ML Naive Bayes classifier
        detected_price_col = logic.target_price_column_only(numeric_cols)

        # AUTOMATIC SELECTION: No tabs, dropdowns, or selection elements anywhere in the user interface
        # System automatically assigns values bypassing UI hooks entirely
        chosen_num = detected_price_col if detected_price_col in numeric_cols else (
            numeric_cols[0] if numeric_cols else None)
        chosen_text = text_cols[0] if text_cols else None

        # Coordinate data operations based on user selection
        if chosen_num:
            calculated_metrics = logic.process_analytics(df, chosen_num)
            frontend.display_numeric_dashboard(calculated_metrics, chosen_num)

        if chosen_text:
            text_distribution_df = logic.calculate_text_distribution(df, chosen_text)
            frontend.st.dataframe(text_distribution_df)

        # Trigger email automation routines when submit action requirements are confirmed
        if submit_clicked and user_email:
            # Consolidate latest calculations state packet values safely
            fallback_col = chosen_num if chosen_num else (numeric_cols[0] if numeric_cols else None)

            if fallback_col:
                final_report_data = logic.process_analytics(df, fallback_col)
                mailer.dispatch_analytics_report(user_email, final_report_data)
                st.success(f"📬 Analytical report has been queued for transmission to: {user_email}")
            else:
                st.error("Cannot dispatch email report: No valid numeric column exists to calculate metrics.")

    else:
        frontend.display_empty_warning()
