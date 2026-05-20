import streamlit as st


def render_base_uploader_ui():
    """Renders page identity headers and files extraction blocks."""
    st.title("Unified Data & Text Analyzer")
    uploaded_files = st.file_uploader(
        "Upload files", type=["csv", "xlsx", "xls", "txt"], accept_multiple_files=True
    )
    email = st.text_input("📬 Enter your email address:", placeholder="your-email@example.com")
    submit_button = st.button("🚀 Run Analytics & Email Report")
    return uploaded_files, email, submit_button


def render_data_tabs_layout(numeric_cols, text_cols, detected_col_name):
    """Renders the high-level structural tabs layout selection logic."""
    tab1, tab2 = st.tabs(["🔢 Numeric Metrics", "🔤 Text Element Counter"])

    selected_num_col = None
    selected_text_col = None

    with tab1:
        if numeric_cols:
            st.subheader("Price Metrics Breakdown")
            default_idx = numeric_cols.index(detected_col_name) if detected_col_name in numeric_cols else 0
            selected_num_col = st.selectbox("Select a numeric column:", numeric_cols, index=default_idx)
        else:
            st.info("No numeric columns found in this dataset.")

    with tab2:
        if text_cols:
            st.subheader("Identical Element Counts")
            selected_text_col = st.selectbox("Select a text column to isolate elements:", text_cols)
        else:
            st.info("No text columns found in this dataset.")

    return selected_num_col, selected_text_col


def display_numeric_dashboard(metrics, selected_col):
    """Draws a balanced 2x2 presentation layout container for metrics numbers."""
    if metrics["transaction_count"] > 0:
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        row1_col1.metric(label=f"Highest Price ({selected_col})", value=f"${metrics['highest_price']:,.2f}")
        row1_col2.metric(label=f"Lowest Price ({selected_col})", value=f"${metrics['lowest_price']:,.2f}")
        row2_col1.metric(label=f"Average Price ({selected_col})", value=f"${metrics['average_price']:,.2f}")
        row2_col2.metric(label="Standard Deviation", value=f"{metrics['standard_deviation']:,.2f}")
    else:
        st.warning("The selected column contains no valid numeric data records.")


def display_text_table(counts_df):
    """Outputs structured table layouts safely inside the DOM wrapper."""
    st.dataframe(counts_df, use_container_width=True)


def display_empty_warning():
    st.warning("Uploaded files do not contain usable data layouts.")
