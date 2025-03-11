''' Main file for the backend '''
import os
from flask import Flask

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    """
    Return a welcome message for the API homepage.
    """
    return {"message": "Hello from the backend!"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5515, debug=True)
