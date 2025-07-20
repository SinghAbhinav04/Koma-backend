# app.py
from flask import Flask
from routes.auth import auth_bp
from routes.manga import manga_bp
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(manga_bp, url_prefix="/koma")

if __name__ == "__main__":
    app.run(debug=True)
