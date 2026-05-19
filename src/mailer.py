import resend
import streamlit as st


def send_summary_email(recipient_email, total_sales, column_name, file_names):
    """
    Authenticates with Streamlit secrets and dispatches reports via Resend.
    """
    if "RESEND_API_KEY" not in st.secrets:
        raise RuntimeError("Missing 'RESEND_API_KEY' inside secrets configuration.")

    resend.api_key = st.secrets["RESEND_API_KEY"]

    html_content = f"""
    <h2>Your Combined Data Analytics Report is Ready!</h2>
    <p><strong>Processed Files:</strong> {', '.join(file_names)}</p>
    <hr />
    <p><strong>Selected Revenue Column:</strong> {column_name}</p>
    <p style="font-size: 18px; color: #2e7d32;">
        <strong>Total Combined Sales:</strong> ${total_sales:,.2f}
    </p>
    <hr />
    <p><small>Generated automatically by your Data Analytics Web App.</small></p>
    """

    return resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": recipient_email,
        "subject": "📊 Your Combined Data Analytics Summary",
        "html": html_content
    })
