import streamlit as st
from email_utils import check_email

st.title("Email Validator")

email = st.text_input("Enter an email to validate:")
if email:
    result = check_email(email)
    if "error" in result:
        st.error(result["error"])
    else:
        st.json(result)
