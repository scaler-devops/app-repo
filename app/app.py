from flask import Flask
import os

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "v1")

@app.route("/")
def home():
    return f"Hello from CI/CD + GitOps demo! Version: {VERSION}\n"

@app.route("/healthz")
def health():
    return "OK\n", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

