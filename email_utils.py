import requests

ABSTRACT_API_KEY = "784d1d7d572640059eaeb0c42490b4b3"

def check_email(email):
    url = f"https://emailvalidation.abstractapi.com/v1/?api_key={ABSTRACT_API_KEY}&email={email}"
    print("DEBUG URL:", url)  # Optional for testing
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
        return {"error": f"Failed to validate email. Status code: {response.status_code}"}
