from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_cors import CORS
import os
import sys


CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:3000"]}})

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route("/", methods=["GET"])
def get_hey():
    print("Root endpoint hit!")
    return "hey from Koma", 200

# Try to import blueprints with error handling
try:
    print("Attempting to import auth blueprint...")
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    print("Auth blueprint registered successfully")
except Exception as e:
    print(f"Failed to import auth blueprint: {e}")

try:
    print("Attempting to import manga blueprint...")
    from routes.manga import manga_bp
    app.register_blueprint(manga_bp, url_prefix="/koma")
    print("Manga blueprint registered successfully")
except Exception as e:
    print(f"Failed to import manga blueprint: {e}")

print("Flask app setup complete!")

if __name__ == "__main__":
    load_dotenv()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
