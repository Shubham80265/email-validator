import re
import dns.resolver
import smtplib
import socket

# Load disposable domain list
with open("disposable_domains.txt", "r") as f:
    DISPOSABLE_DOMAINS = set(line.strip() for line in f if line.strip())

def is_valid_format(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None

def has_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, "MX")
        return len(answers) > 0
    except Exception:
        return False

def is_disposable(email):
    domain = email.split("@")[1].lower()
    return domain in DISPOSABLE_DOMAINS

def smtp_check(email, from_address="noreply@example.com", timeout=10):
    domain = email.split("@")[1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(sorted(mx_records, key=lambda r: r.preference)[0].exchange)
        server = smtplib.SMTP(timeout=timeout)
        server.connect(mx_host)
        server.helo("example.com")
        server.mail(from_address)
        code, message = server.rcpt(email)
        server.quit()
        return code == 250 or code == 251
    except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError, socket.timeout, dns.exception.DNSException):
        return None

def check_email(email):
    result = {
        "email": email,
        "format_valid": False,
        "has_mx": False,
        "smtp_valid": None,
        "disposable": False,
        "catch_all": False,
        "valid": False
    }
    if not is_valid_format(email):
        return result
    result["format_valid"] = True
    domain = email.split("@")[1]
    result["has_mx"] = has_mx_record(domain)
    result["disposable"] = is_disposable(email)
    if result["has_mx"]:
        smtp_result = smtp_check(email)
        result["smtp_valid"] = smtp_result
        if smtp_result is None:
            result["catch_all"] = True
        elif smtp_result:
            result["valid"] = True
    return result

if __name__ == "__main__":
    email = input("Enter an email to check: ")
    result = check_email(email)
    for k, v in result.items():
        print(f"{k}: {v}")