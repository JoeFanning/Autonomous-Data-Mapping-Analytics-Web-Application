import streamlit as st

def render_ui():
    """Renders the website elements and returns the user inputs."""
    st.set_page_config(page_title="Data Analytics Web App", page_icon="📊")
    st.title("📊 Data Analytics Web App")
    st.write("Upload your Excel or CSV files. We will combine them, run analytics, and email you the report!")
    
    # Draw input spaces
    email = st.text_input("📬 Enter your email address:", placeholder="your-email@example.com")
    files = st.file_uploader(
        "📁 Upload your spreadsheets (CSV or XLSX):", 
        type=["csv", "xlsx"], 
        accept_multiple_files=True
    )
    
    submit_button = st.button("🚀 Run Analytics & Email Report")
    
    return email, files, submit_button

