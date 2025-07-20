# routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.jwt_handler import generate_token
from models.user_schema import create_user, find_user_by_email_or_username
from utils.encrypt_decrypt import encrypt_api_key

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    username = data.get("username")
    dob = data.get("dob")
    password = data.get("password")
    api_key = data.get("api")

    if find_user_by_email_or_username(email) or find_user_by_email_or_username(username):
        return jsonify({"error": "User already exists"}), 409

    password_hash = generate_password_hash(password)
    api_cipher = encrypt_api_key(api_key)

    user = create_user(name, email, username, dob, password_hash , api_cipher)
    token = generate_token(user.inserted_id)
    return jsonify({"message": "Signup successful", "token": token}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    identifier = data.get("identifier")  # username or email
    password = data.get("password")

    user = find_user_by_email_or_username(identifier)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user["_id"])
    return jsonify({"message": "Login successful", "token": token})
