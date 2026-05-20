import streamlit as st
# Explicitly route imports into your 'src' directory structure
from src import frontend  # Owns the UI Look
from src import logic  # Owns the ML & Math Data Brain
from src import mailer  # Owns the Email Dispatch Delivery

# 1. Run the base web UI interface setup tools
uploaded_files, user_email, submit_clicked = frontend.render_base_uploader_ui()

if uploaded_files:

    # Caching helper layer sits safely inside control loop routing parameters
    @st.cache_data(show_spinner="Combining and loading dataset structures...")
    def process_raw_files(files):
        return logic.merge_and_load_spreadsheets(files)


    df = process_raw_files(uploaded_files)

    # Clean file pointers immediately after memory conversion pipeline routines
    for f in uploaded_files:
        f.seek(0)

    if not df.empty:
        # Determine internal pandas core structural components
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        text_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        # Route numeric attributes downstream into backend ML Naive Bayes classifier
        detected_price_col = logic.target_price_column_only(numeric_cols)

        # Tell the UI to render tabs, receiving selected columns back
        chosen_num, chosen_text = frontend.render_data_tabs_layout(
            numeric_cols, text_cols, detected_price_col
        )

        # Coordinate data operations based on user selection
        if chosen_num:
            calculated_metrics = logic.process_analytics(df, chosen_num)
            frontend.display_numeric_dashboard(calculated_metrics, chosen_num)

        if chosen_text:
            text_distribution_df = logic.calculate_text_distribution(df, chosen_text)
            frontend.display_text_table(text_distribution_df)

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
