import streamlit as st


def render_base_uploader_ui():
    """Renders page identity headers and files extraction blocks."""
    st.title("Autonomous Data Mapping & Analytics")
    # Use a Markdown header to make the text large and bold
    st.markdown("### 📁 Upload your Excel (.xlsx) or CSV (.csv) files")
    st.write("We will combine them, run analytics, and email you the report!")

    # Set label_visibility to "collapsed" to hide the small default label
    uploaded_files = st.file_uploader(
        label="Upload Space",
        label_visibility="collapsed",
        type=["csv", "xlsx", "xls", "txt"],
        accept_multiple_files=True
    )

    email = st.text_input("📬 Enter your email address:", placeholder="your-email@example.com")
    submit_button = st.button("🚀 Run Analytics & Email Report")
    return uploaded_files, email, submit_button





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
