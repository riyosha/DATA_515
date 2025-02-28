from flask import Flask
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise ValueError("Missing GEMINI_API_KEY! Set it in your .env file.")

# print(f"Using Google Gemini API Key: {GEMINI_API_KEY[:5]}... (hidden for security)")

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Hello from the backend!"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5515, debug=True)
