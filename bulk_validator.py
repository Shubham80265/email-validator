HEAD
import streamlit as st
import pandas as pd
import re
import dns.resolver
import matplotlib.pyplot as plt

# Load disposable domains list
@st.cache_data
def load_disposable_domains():
    with open("disposable_domains.txt", "r") as f:
        return set(line.strip().lower() for line in f if line.strip())

DISPOSABLE_DOMAINS = load_disposable_domains()

def is_valid_format(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None

def has_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=5.0)
        return len(answers) > 0
    except dns.resolver.NXDOMAIN:
        return False
    except dns.resolver.Timeout:
        return False
    except Exception as e:
        print(f"MX check failed for {domain}: {e}")
        return False

def is_disposable(email):
    domain = email.split("@")[1].lower()
    return domain in DISPOSABLE_DOMAINS

def validate_email(email, check_mx=True):
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
    result["has_mx"] = has_mx_record(domain) if check_mx else True
    result["is_disposable"] = is_disposable(email)
    result["valid"] = result["format_valid"] and result["has_mx"] and not result["is_disposable"]

    return result

# --- Streamlit Interface ---
st.title("📧 Email Validator Tool")

tabs = st.tabs(["🔍 Single Email", "📂 Bulk Upload"])

# --- Single Email Tab ---
with tabs[0]:
    st.header("Single Email Validator")
    email = st.text_input("Enter an email to validate:")
    check_mx = st.checkbox("Check MX records (slower, more accurate)", value=True)
    if email:
        result = validate_email(email, check_mx=check_mx)
        st.json(result)

# --- Bulk Upload Tab ---
with tabs[1]:
    st.header("Bulk Email Validator")
    uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"Uploaded file with {df.shape[0]} rows and {df.shape[1]} columns.")

        email_column = st.selectbox("Select the column containing email addresses:", df.columns)
        check_mx_bulk = st.checkbox("Check MX records for each email", value=True)

        if st.button("✅ Validate Emails"):
            emails = df[email_column].dropna().astype(str).unique()
            st.write(f"Found {len(emails)} unique email(s) to validate.")

            results = []
            progress_bar = st.progress(0)

            for idx, email in enumerate(emails):
                result = validate_email(email, check_mx=check_mx_bulk)
                results.append(result)
                progress_bar.progress((idx + 1) / len(emails))

            result_df = pd.DataFrame(results)
            st.subheader("🔍 Validation Results")
            st.dataframe(result_df)

            # Pie chart summary
            st.subheader("📊 Summary Chart")
            pie_data = result_df["valid"].value_counts().rename(index={True: "Valid", False: "Invalid"})
            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            st.pyplot(fig)

            # Download button
            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="validated_emails.csv",
                mime="text/csv"
            )
import streamlit as st
import pandas as pd
import re
import dns.resolver
import matplotlib.pyplot as plt

# Load disposable domains list
@st.cache_data
def load_disposable_domains():
    with open("disposable_domains.txt", "r") as f:
        return set(line.strip().lower() for line in f if line.strip())

DISPOSABLE_DOMAINS = load_disposable_domains()

def is_valid_format(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None

def has_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=5.0)
        return len(answers) > 0
    except dns.resolver.NXDOMAIN:
        return False
    except dns.resolver.Timeout:
        return False
    except Exception as e:
        print(f"MX check failed for {domain}: {e}")
        return False

def is_disposable(email):
    domain = email.split("@")[1].lower()
    return domain in DISPOSABLE_DOMAINS

def validate_email(email, check_mx=True):
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
    result["has_mx"] = has_mx_record(domain) if check_mx else True
    result["is_disposable"] = is_disposable(email)
    result["valid"] = result["format_valid"] and result["has_mx"] and not result["is_disposable"]

    return result

# --- Streamlit Interface ---
st.title("📧 Email Validator Tool")

tabs = st.tabs(["🔍 Single Email", "📂 Bulk Upload"])

# --- Single Email Tab ---
with tabs[0]:
    st.header("Single Email Validator")
    email = st.text_input("Enter an email to validate:")
    check_mx = st.checkbox("Check MX records (slower, more accurate)", value=True)
    if email:
        result = validate_email(email, check_mx=check_mx)
        st.json(result)

# --- Bulk Upload Tab ---
with tabs[1]:
    st.header("Bulk Email Validator")
    uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"Uploaded file with {df.shape[0]} rows and {df.shape[1]} columns.")

        email_column = st.selectbox("Select the column containing email addresses:", df.columns)
        check_mx_bulk = st.checkbox("Check MX records for each email", value=True)

        if st.button("✅ Validate Emails"):
            emails = df[email_column].dropna().astype(str).unique()
            st.write(f"Found {len(emails)} unique email(s) to validate.")

            results = []
            progress_bar = st.progress(0)

            for idx, email in enumerate(emails):
                result = validate_email(email, check_mx=check_mx_bulk)
                results.append(result)
                progress_bar.progress((idx + 1) / len(emails))

            result_df = pd.DataFrame(results)
            st.subheader("🔍 Validation Results")
            st.dataframe(result_df)

            # Pie chart summary
            st.subheader("📊 Summary Chart")
            pie_data = result_df["valid"].value_counts().rename(index={True: "Valid", False: "Invalid"})
            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            st.pyplot(fig)

            # Download button
            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="validated_emails.csv",
                mime="text/csv"
            )
5206a34 (Added pie chart and unified local email validator)
