import resend
import streamlit as st


def dispatch_analytics_report(recipient_email, analytics_data):
    """
    Authenticates with Streamlit secrets and dispatches reports via Resend.
    Syncs perfectly with data dictionaries sent from main.py controller loops.
    """
    # 1. Validate secrets configuration parameters
    if "RESEND_API_KEY" not in st.secrets:
        raise RuntimeError("Missing 'RESEND_API_KEY' inside secrets configuration.")

    resend.api_key = st.secrets["RESEND_API_KEY"]

    # 2. Extract metrics safely out of the data packet dict sent by main.py
    # Provide zero fallbacks if the file did not contain numeric information
    total_revenue = analytics_data.get("total_revenue", 0.0)
    highest = analytics_data.get("highest_price", 0.0)
    lowest = analytics_data.get("lowest_price", 0.0)
    average = analytics_data.get("average_price", 0.0)
    median = analytics_data.get("median", 0.0)
    std_dev = analytics_data.get("standard_deviation", 0.0)
    transaction_count = analytics_data.get("transaction_count", 0.0)

    # Compile a metrics dashboard visualization layout directly inside the email body template
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
        <h2 style="color: #1e3a8a; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px;">📊 Autonomous Data Mapping & Analytics</h2>
        <p>Your requested machine learning data analytics pipeline summary is complete.</p>

        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
        <tr style="background-color: #f8fafc;">
                <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">Total Revenue:</td>
                <td style="padding: 12px; border: 1px solid #e2e8f0; color: #10b981; font-weight: bold;">${total_revenue:,.2f}</td>
            </tr>
            <tr style="background-color: #f8fafc;">
                <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">Highest Value Found:</td>
                <td style="padding: 12px; border: 1px solid #e2e8f0; color: #10b981; font-weight: bold;">${highest:,.2f}</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">Lowest Value Found:</td>
                <td style="padding: 12px; border: 1px solid #e2e8f0; color: #ef4444; font-weight: bold;">${lowest:,.2f}</td>
            </tr>
            <tr style="background-color: #f8fafc;">
                <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">Average Value (Mean):</td>
                <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">${average:,.2f}</td>
            </tr>
            <tr style="background-color: #f8fafc;">
                <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">Median:</td>
                <td style="padding: 12px; border: 1px solid #e2e8f0; color: #10b981; font-weight: bold;">${median:,.2f}</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">Standard Deviation Spread:</td>
                <td style="padding: 12px; border: 1px solid #e2e8f0; color: #64748b;">{std_dev:,.2f}</td>
            </tr>
             <tr>
                <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">Transaction Count:</td>
                <td style="padding: 12px; border: 1px solid #e2e8f0; color: #64748b;">{transaction_count:,.2f}</td>
            </tr>
        </table>

        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 25px 0;" />
        <p style="font-size: 12px; color: #94a3b8; text-align: center;">Generated automatically by Autonomous Data Mapping Pipeline Web Application created by Joe Fanning May 2026</p>
    </div>
    """

    # 3. Request delivery execution rules via Resend SDK
    return resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": recipient_email,
        "subject": "📊 Your Combined Data Analytics Summary Report",
        "html": html_content
    })
