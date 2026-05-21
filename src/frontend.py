import streamlit as st


def render_base_uploader_ui():
    """Renders page identity headers and files extraction blocks."""
    st.title("Autonomous Data Mapping & Analytics")
    st.markdown("### 📁 Upload your Excel (.xlsx) or CSV (.csv) files")
    st.write("We will combine them, run analytics, and email you the report!")

    uploaded_files = st.file_uploader(
        label="Upload Space",
        label_visibility="collapsed",
        type=["csv", "xlsx", "xls", "txt"],
        accept_multiple_files=True
    )

    email = st.text_input("📬 Enter your email address:", placeholder="joespirial@hotmail.com")
    submit_button = st.button("🚀 Run Analytics & Email Report")
    if submit_button:
        if not email:
            # Stop everything immediately and alert the user right here
            st.error("⚠️ Please provide a valid email address before running the report.")
            st.stop()
        else:
            submit_clicked = True
    else:
        submit_clicked = False

    return uploaded_files, email, submit_button


def process_and_get_numeric_column(numeric_cols, detected_col_name):
    """Automatically resolves the numeric target column completely behind the scenes."""
    if not numeric_cols:
        return None
    if detected_col_name in numeric_cols:
        return detected_col_name
    return numeric_cols[0]


def display_numeric_dashboard(metrics, selected_col):
    """Draws a balanced 2x2 presentation layout container for metrics numbers."""
    if not selected_col:
        st.info("No numeric columns found in this dataset.")
        return

    st.subheader(f"📊 Analytics Summary for : ({selected_col})")

    if metrics["transaction_count"] > 0:
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        row3_col1, row3_col2 = st.columns(2)

        row1_col1.metric(label=f"Total Revenue ({selected_col})", value=f"${metrics['total_revenue']:,.2f}")
        row1_col2.metric(label=f"Highest Price ({selected_col})", value=f"${metrics['highest_price']:,.2f}")
        row2_col1.metric(label=f"Lowest Price ({selected_col})", value=f"${metrics['lowest_price']:,.2f}")
        row2_col2.metric(label=f"Average Price ({selected_col})", value=f"${metrics['average_price']:,.2f}")
        row3_col1.metric(label=f"Geometric Mean ({selected_col})", value=f"${metrics['geometric_mean']:,.2f}")
        row3_col2.metric(label="Standard Deviation", value=f"{metrics['standard_deviation']:,.2f}")

    else:
        st.warning("Please upload an Excel file with transactional or sales data. Your file has no numbers to calculate")


def display_empty_warning():
    st.warning("Uploaded files do not contain usable data layouts.")
