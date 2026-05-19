import streamlit as st
import pandas as pd
from src import logic
from src import mailer

# Setup layout
st.set_page_config(page_title="Data Analytics Web App", page_icon="📊")
st.title("📊 Data Analytics Web App")
st.write("Upload your Excel or CSV files. We will combine them, run analytics, and email you the report!")

# Inputs
email = st.text_input("📬 Enter your email address:", placeholder="your-email@example.com")
uploaded_files = st.file_uploader("📁 Upload spreadsheets:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    combined_list = []
    file_names = [f.name for f in uploaded_files]

    for file in uploaded_files:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        combined_list.append(df)

    final_df = pd.concat(combined_list, ignore_index=True)
    st.success(f"Successfully loaded {len(uploaded_files)} files!")

    st.subheader("Map Your Data Columns")
    sales_column = st.selectbox("Select your Sales/Revenue column:", final_df.columns)

    if sales_column:
        st.subheader("📈 Quick Analytics Summary")

        try:
            # Execute logic module
            results = logic.process_analytics(final_df, sales_column)

            st.metric(label="Total Sales Across Combined Files", value=f"${results['total_sales']:,.2f}")
            st.write("Combined Data Preview:", final_df.head())

            # Action execution
            st.subheader("📬 Send Report")
            if not email:
                st.warning("Please enter an email address above to unlock submission.")
            else:
                if st.button("📨 Process & Email Report"):
                    with st.spinner("Sending email..."):
                        # Execute mailer module
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
