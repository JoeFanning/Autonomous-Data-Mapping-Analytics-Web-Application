import streamlit as st
import frontend
import analytics
import emailer

# 1. Draw the UI and collect the inputs
user_email, uploaded_files, clicked = frontend.render_ui()

# 2. Watch for the button click event
if clicked:
    if not user_email:
        st.error("Please enter a valid email address first.")
    elif not uploaded_files:
        st.error("Please upload at least one CSV or Excel file.")
    else:
        with st.spinner("Processing files and sending email..."):
            try:
                # 3. Pass data to the Backend Logic module
                results = analytics.process_and_combine_files(uploaded_files)
                
                # 4. Fetch safe app secrets
                gmail_user = st.secrets["EMAIL_USER"]
                gmail_pass = st.secrets["EMAIL_PASSWORD"]
                
                # 5. Pass data to the Emailer module
                emailer.send_report_email(user_email, gmail_user, gmail_pass, results)
                
                # 6. Notify user of success
                st.success(f"🎉 Success! The report has been sent to {user_email}.")
                st.write("### Preview of Your Combined Data Summary:")
                st.text(results['summary_stats'])
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")

