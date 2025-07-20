# routes/auth.py
from aiohttp import Payload
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.jwt_handler import generate_token , decode_token
from models.user_schema import create_user, find_user_by_email_or_username , users , comics
from utils.encrypt_decrypt import encrypt_api_key
from bson.objectid import ObjectId

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

@auth_bp.route("/me", methods=["GET"])
def authenticate_me():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    if not token:
        return jsonify({"error": "No authentication token found"}), 401
    
    try:
        payload = decode_token(token)
        user_id = payload["user_id"]

        user = users.find_one({"_id": ObjectId(user_id)}, {"password_hash": 0, "api_cipher": 0})
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Convert ObjectId to string for JSON serialization
        user["_id"] = str(user["_id"])
        
        return jsonify({"user": user}), 200

    except Exception as e:
        print("Token verification error:", e)
        return jsonify({"error": "Invalid or expired token"}), 401

@auth_bp.route("/profile", methods=["GET"])
def get_profile():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        payload = decode_token(token)
        user_id = payload["user_id"]

        user = users.find_one({"_id": ObjectId(user_id)}, {"password_hash": 0, "api_cipher": 0})
        if not user:
            return jsonify({"error": "User not found"}), 404

        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        return jsonify(user), 200

    except Exception as e:
        print("Profile fetch error:", e)
        return jsonify({"error": "Invalid or expired token"}), 401


@auth_bp.route("/delete", methods=["DELETE"])
def delete_account():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        payload = decode_token(token)
        user_id = payload["user_id"]

        # Delete comics by this user
        comics.delete_many({"user_id": ObjectId(user_id)})
        # Delete user
        users.delete_one({"_id": ObjectId(user_id)})

        return jsonify({"message": "Account deleted successfully"}), 200

    except Exception as e:
        print("Delete error:", e)
        return jsonify({"error": "Invalid or expired token"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        decode_token(token)  # Just check token validity
        return jsonify({"message": "Logout successful. Please clear token client-side."}), 200
    except Exception:
        return jsonify({"error": "Invalid or expired token"}), 401
