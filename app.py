import streamlit as st
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

st.title("📧 Single Email Validator (Offline)")

email = st.text_input("Enter an email to validate:")
if email:
    result = check_email(email)
    st.subheader("🔍 Validation Result")
    st.json(result)
