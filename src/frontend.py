import streamlit as st


def render_ui():
    """Renders the core website elements and returns the user inputs."""
    st.title("📊 Enix Data Analytics")
    st.write("Upload your **Excel(.xlsx)** or **CSV(.csv)** files. We will combine them, run analytics, and email you the report!")

    # Draw input spaces
    email = st.text_input("📬 Enter your email address:", placeholder="your-email@example.com")

    # 1. Render the text using st.markdown to successfully force the bold words
    st.markdown("📁 Upload your spreadsheets (**CSV** or **Excel**):")

    # 2. Leave the uploader label empty so it skips the plain text title block
    files = st.file_uploader(
        label="Spreadsheet Upload Space",
        label_visibility="collapsed",
        type=["csv", "xlsx"],
        accept_multiple_files=True
    )

    # The submit button acts as a visual anchor; execution logic resides in main.py
    submit_button = st.button("🚀 Run Analytics & Email Report")

    return email, files, submit_button
