from flask import Flask, request, jsonify
from email_utils import check_email

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Email Validator API is running!"

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    result = check_email(email)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
