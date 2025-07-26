import streamlit as st
import pandas as pd
import requests
import io

ABSTRACT_API_KEY = "784d1d7d572640059eaeb0c42490b4b3"

def check_email(email):
    url = f"https://emailvalidation.abstractapi.com/v1/?api_key={ABSTRACT_API_KEY}&email={email}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "email": email,
                "is_valid_format": data.get("is_valid_format", {}).get("value", False),
                "is_disposable": data.get("is_disposable_email", {}).get("value", False),
                "is_free": data.get("is_free_email", {}).get("value", False),
                "deliverability": data.get("deliverability", "UNKNOWN"),
                "quality_score": data.get("quality_score", "0.0")
            }
        else:
            return {"email": email, "error": f"Status code: {response.status_code}"}
    except Exception as e:
        return {"email": email, "error": str(e)}

st.title("📧 Bulk Email Validator")

uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    # Load file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success(f"Uploaded file with {df.shape[0]} rows and {df.shape[1]} columns.")

    # Column selector
    email_column = st.selectbox("Select the column containing email addresses:", df.columns)

    if st.button("✅ Validate Emails"):
        emails = df[email_column].dropna().astype(str).unique()
        st.write(f"Found {len(emails)} unique email(s) to validate.")

        results = []
        progress_bar = st.progress(0)

        for idx, email in enumerate(emails):
            result = check_email(email)
            results.append(result)
            progress_bar.progress((idx + 1) / len(emails))

        result_df = pd.DataFrame(results)
        st.subheader("🔍 Validation Results")
        st.dataframe(result_df)

        # Enable download
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="validated_emails.csv",
            mime="text/csv"
        )
