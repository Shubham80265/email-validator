import streamlit as st
import pandas as pd
from email_utils import check_email

st.set_page_config(page_title="Email Validator", layout="centered")

st.title("📧 Email Validator Tool")
st.markdown("Upload a file with emails and validate format, domain, SMTP, disposable check, and more.")

uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"❌ Failed to read file: {e}")
        st.stop()

    if 'Email' not in df.columns:
        st.error("⚠️ File must contain an 'Email' column.")
    else:
        st.success("✅ File uploaded successfully.")
        results = []
        with st.spinner("🔍 Validating emails..."):
            for email in df['Email']:
                result = check_email(str(email))
                results.append(result)

        result_df = pd.DataFrame(results)
        st.dataframe(result_df)

        # Download button
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results as CSV", data=csv, file_name="validated_emails.csv", mime="text/csv")

        # Charts
        st.subheader("📊 Summary Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Valid Emails", result_df['valid'].sum())
            st.metric("Catch-All Suspected", result_df['catch_all'].sum())
        with col2:
            st.metric("Disposable Emails", result_df['disposable'].sum())
            st.metric("Invalid Format", (~result_df['format_valid']).sum())