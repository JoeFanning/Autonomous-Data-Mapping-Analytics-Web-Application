import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_report_email(recipient_email, sender_email, sender_password, metrics):
    """Formats and sends the analytics report via Gmail SMTP."""
    email_body = f"""
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
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "📊 Your Automated Data Analytics Report"
    msg.attach(MIMEText(email_body, 'plain'))
    
    with smtplib.SMTP("://gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

