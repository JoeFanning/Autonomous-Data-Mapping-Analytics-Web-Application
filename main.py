import streamlit as st
import pandas as pd

# Import structural components from your three project layers
from src.frontend import render_ui, target_price_column_only
from src.logic import merge_and_load_spreadsheets, process_analytics
from src.mailer import send_summary_email


def main():
    # 1. Page Configuration
    st.set_page_config(page_title="Enix Data Analytics", layout="wide")

    # 2. State Maintenance
    if "combined_df" not in st.session_state:
        st.session_state.combined_df = None

    # 3. Component Rendering (frontend.py)
    email, uploaded_files, submit_clicked = render_ui(df=st.session_state.combined_df)

    # 4. Pipeline Syncing Engine (logic.py)
    if uploaded_files:
        try:
            merged_df = merge_and_load_spreadsheets(uploaded_files)

            for f in uploaded_files:
                f.seek(0)

            if st.session_state.combined_df is None or not st.session_state.combined_df.equals(merged_df):
                st.session_state.combined_df = merged_df
                st.rerun()

        except Exception as e:
            st.error(f"Error compiling spreadsheet datasets: {e}")

    else:
        st.session_state.combined_df = None

    # 5. Report Dispatch Engine (mailer.py)
    if submit_clicked:
        if not email:
            st.error("⚠️ Please enter a valid recipient email address first.")
        elif not uploaded_files or st.session_state.combined_df is None:
            st.error("⚠️ Please upload your analytics spreadsheet source files first.")
        else:
            with st.spinner("Calculating dataset matrices and dispatching email report..."):
                df = st.session_state.combined_df
                numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

                detected_price_col = target_price_column_only(numeric_cols)

                if detected_price_col:
                    try:
                        metrics_data = process_analytics(df, detected_price_col)
                        total_sales = metrics_data["total_sales"]
                        file_names = [f.name for f in uploaded_files]

                        send_summary_email(
                            recipient_email=email,
                            total_sales=total_sales,
                            column_name=detected_price_col,
                            file_names=file_names
                        )

                        st.success(f"🎉 Success! Analytical summary report successfully dispatched to {email}")

                    except RuntimeError as e:
                        st.error(f"Configuration Error: {e}")
                        st.info(
                            "💡 Please specify a `RESEND_API_KEY` token inside your `.streamlit/secrets.toml` parameters.")
                    except Exception as e:
                        st.error(f"Email Dispatch Failure: {e}")
                else:
                    st.error(
                        "❌ Aborted: Could not find any valid financial target metrics inside the uploaded file columns.")


if __name__ == "__main__":
    main()
