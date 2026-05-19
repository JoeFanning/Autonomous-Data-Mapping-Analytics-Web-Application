import base64
import os
import resend

def send_report_email(recipient_email, api_key, metrics):
    """Formats and sends the analytics report using Resend SDK."""
    
    # 1. Initialize the official Resend client
    resend.api_key = api_key

    # 2. Build the email body text
    body_text = f"""
    Hello,

    Your automated data analytics report is ready!

    --- SUMMARY INFO ---
    * Total files combined: {metrics['total_files']}
    * Total rows processed: {metrics['total_rows']}
    * Total columns found: {metrics['total_columns']}

    --- NUMERICAL DATA STATS ---
    {metrics['summary_stats']}

    Thank you for using the Data Analytics Web App!
    """

    # 3. Convert plaintext formatting to HTML for Resend
    html_body = f"<div style='font-family: Arial, sans-serif; white-space: pre-wrap;'>{body_text}</div>"

    # 4. Construct the Resend payload
    email_params = {
        "from": "Automation Engine <onboarding@resend.dev>",
        "to": [recipient_email],
        "subject": "📊 Your Automated Data Analytics Report",
        "html": html_body
    }

    # 5. Transmit the email via Resend Cloud
    # (Note: If you want to attach the combined file, we can add that next!)
    email_response = resend.Emails.send(email_params)
    return email_response
