import streamlit as st
import pandas as pd
import re
import dns.resolver

# Load disposable domains list from file
def load_disposable_domains():
    with open("disposable_domains.txt", "r") as f:
        return set(line.strip().lower() for line in f if line.strip())

DISPOSABLE_DOMAINS = load_disposable_domains()

def is_valid_format(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None

def has_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, "MX")
        return len(answers) > 0
    except:
        return False

def is_disposable(email):
    domain = email.split("@")[1].lower()
    return domain in DISPOSABLE_DOMAINS

def check_email(email):
    result = {
        "email": email,
        "format_valid": is_valid_format(email),
        "has_mx": False,
        "is_disposable": False,
        "valid": False
    }

    if not result["format_valid"]:
        return result

    domain = email.split("@")[1]
    result["has_mx"] = has_mx_record(domain)
    result["is_disposable"] = is_disposable(email)
    result["valid"] = result["format_valid"] and result["has_mx"] and not result["is_disposable"]

    return result

st.title("📧 Bulk Email Validator (Offline)")

uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success(f"Uploaded file with {df.shape[0]} rows and {df.shape[1]} columns.")

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

        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="validated_emails.csv",
            mime="text/csv"
        )
