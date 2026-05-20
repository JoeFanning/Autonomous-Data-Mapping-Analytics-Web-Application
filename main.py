import streamlit as st
import pandas as pd
from src import frontend
from src import logic
from src import mailer

# ALWAYS FIRST: Setup page configuration at the root level
st.set_page_config(page_title="Enix Data Analytics", page_icon="📊")

# Render UI elements from the src/frontend module
email, uploaded_files, submit_button = frontend.render_ui()

if uploaded_files:
    file_names = [f.name for f in uploaded_files]

    try:
        # Offload file parsing and concatenation to the logic module
        final_df = logic.merge_and_load_spreadsheets(uploaded_files)
        st.success(f"Successfully loaded {len(uploaded_files)} files!")

        st.subheader("Map Your Data Columns")

        # --- INSERTED NUMERIC FILTERING LOGIC HERE ---
        # Filter the dataframe to only keep columns containing numbers
        numeric_df = final_df.select_dtypes(include=["number"])
        numeric_columns = numeric_df.columns.tolist()

        if not numeric_columns:
            st.error("❌ No numeric columns were detected in your uploaded files.")
        else:
            # Pass only the filtered numeric column names to the selectbox
            sales_column = st.selectbox("Select your Sales/Revenue column:", numeric_columns)
            # ---------------------------------------------

            if sales_column:
                st.subheader("📈 Quick Analytics Summary")

                # Offload metrics calculation to the logic module
                results = logic.process_analytics(final_df, sales_column)

                # Display UI metrics
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Total Sales", value=f"${results['total_sales']:,.2f}")
                col2.metric(label="Average Sales", value=f"${results['average_sales']:,.2f}")
                col3.metric(label="Transaction Count", value=f"{results['transaction_count']:,}")

                st.write("Combined Data Preview:", final_df.head())

                # Trigger notification workflow
                if submit_button:
                    if not email:
                        st.warning("Please enter an email address to receive the report.")
                    else:
                        with st.spinner("Sending email..."):
                            mailer.send_summary_email(
                                recipient_email=email,
                                total_sales=results['total_sales'],
                                column_name=sales_column,
                                file_names=file_names
                            )
                            st.success(f"🚀 Success! Report emailed cleanly to **{email}**.")

    except ValueError as val_err:
        st.error(f"❌ Data Error: {val_err}")
    except Exception as e:
        st.error(f"⚠️ App Encountered an Error: {e}")
