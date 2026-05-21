import streamlit as st
# Explicitly route imports into your 'src' directory structure
from src import frontend  # Owns the UI Look
from src import logic  # Owns the ML & Math Data Brain
from src import mailer  # Owns the Email Dispatch Delivery

# 1. Run the base web UI interface setup tools
uploaded_files, user_email, submit_clicked = frontend.render_base_uploader_ui()

if uploaded_files:

    # @st.cache_data: This is a Streamlit decorator. It saves (caches) the output of the function
    # in your computer's memory based on the input files.
    # show_spinner="...": This displays a temporary loading message and spinner on the user's screen
    # while the function runs for the first time.
    @st.cache_data(show_spinner="Combining and loading dataset structures...")
    #  This defines the helper function that accepts a list of raw files.
    def process_raw_files(files):
        # A Streamlit function. This calls an external custom script (logic) to
        # combine and format the spreadsheets into a unified dataset.
        return logic.merge_and_load_spreadsheets(files)

    # This line of code executes the caching function and stores the final, combined dataset into
    # a pandas DataFrame named df
    df = process_raw_files(uploaded_files)

    #File Reading Concept: Python treats uploaded files like a VHS tape or a physical book. When a
    # function (like your process_raw_files) reads a file, it moves an internal cursor from the beginning to the end.
    # The "Empty File" Trap: If you try to read the file a second time without resetting it, Python starts reading from
    # the very end of the file. This results in an empty string or an empty DataFrame, often causing silent bugs or crashes.
    # f.seek(0): This forces the cursor back to the start line. It allows you to safely re-read, validate, or process the
    # same uploaded files multiple times within your app.
    for f in uploaded_files:
        f.seek(0)
    # if not df.empty:: This acts as a safety guard. It ensures the DataFrame actually contains rows and columns before
    # trying to analyze it, preventing errors if the uploaded files were blank.
    # if not df.empty:: This acts as a safety guard. It ensures the DataFrame actually contains rows and columns before
    # trying to analyze it, preventing errors if the uploaded files were blank.
    if not df.empty:
        # df.select_dtypes(...): This is a pandas method that filters your DataFrame columns by their data types
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        text_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        # Route numeric attributes downstream into backend ML Naive Bayes classifier
        detected_price_col = logic.target_price_column_only(numeric_cols)

        # AUTOMATIC SELECTION: No tabs, dropdowns, or selection elements anywhere in the user interface
        chosen_num = detected_price_col if detected_price_col in numeric_cols else (
            numeric_cols if numeric_cols else None)
        chosen_text = text_cols if text_cols else None

        # Coordinate data operations based on user selection
        if chosen_num:
            calculated_metrics = logic.process_analytics(df, chosen_num)
            frontend.display_numeric_dashboard(calculated_metrics, chosen_num)

        if chosen_text:
            text_distribution_df = logic.calculate_text_distribution(df, chosen_text)
            st.write("### Text Column Distribution")
            st.dataframe(text_distribution_df, use_container_width=True)

        # --- DEBUG AREA: Let's track if variables are surviving the button click ---
        # st.write(f"Debug - Submit status: {submit_clicked}, Email entered: '{user_email}'")

        # Trigger email automation routines when submit action requirements are confirmed
            # Trigger email automation routines when submit action requirements are confirmed
            if submit_clicked:
                if not user_email:
                    st.toast("⚠️ Please provide an email address before running the report.", icon="⚠️")
                else:
                    # Consolidate latest calculations state packet values safely
                    fallback_col = chosen_num if chosen_num else (numeric_cols if numeric_cols else None)

                    if fallback_col:
                        # st.toast creates a floating popup notification in the lower right corner instantly
                        st.toast("🔄 Processing final analytics and contacting Resend servers...", icon="🔄")
                        try:
                            final_report_data = logic.process_analytics(df, fallback_col)
                            mailer.dispatch_analytics_report(user_email, final_report_data)

                            # Use toast + an explicit main page success header so the user can definitely see it
                            st.toast("📬 Analytics report successfully dispatched!", icon="📬")
                            st.write(f"### 🎉 Success! Report sent to **{user_email}**")

                        except Exception as e:
                            st.toast(f"❌ Mailer execution failed: {e}", icon="❌")
                            st.error(f"❌ Detailed Mailer Crash Log: {e}")
                    else:
                        st.toast("❌ No valid numeric column found to calculate metrics.", icon="❌")

        else:
            frontend.display_empty_warning()

