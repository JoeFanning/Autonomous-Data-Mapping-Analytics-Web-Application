import streamlit as st
from src import frontend
from src import logic
from src import mailer
import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env file if it exists
load_dotenv()

# Fetch your key from the environment
resend_key = os.environ.get("RESEND_API_KEY")

if not resend_key:
    st.error("API Key not found!")

# 1. Draw the UI and collect the inputs
user_email, uploaded_files, clicked = frontend.render_ui()

# 2. Watch for the button click event
if clicked:
    if not user_email:
        st.error("Please enter a valid email address first.")
    elif not uploaded_files:
        st.error("Please upload at least one CSV or Excel file.")
    else:
        with st.spinner("Processing files and transmitting email via Resend..."):
            try:
                # 3. Pass data to the Backend Logic module
                results = logic.process_and_combine_files(uploaded_files)
                
                # 4. Fetch safe app secrets (Resend Key)
                resend_api_key = st.secrets["RESEND_API_KEY"]
                
                # 5. Pass data to the Resend Emailer module
                mailer.send_report_email(user_email, resend_api_key, results)
                
                # 6. Notify user of success
                st.success(f"🎉 Success! The report has been sent to {user_email} via Resend.")
                st.write("### Preview of Your Combined Data Summary:")
                st.text(results['summary_stats'])
                
            except Exception as e:
                st.error(f"Something went wrong during execution: {e}")

