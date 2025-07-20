# models/user_schema.py
from utils.encrypt_decrypt import decrypt_api_key
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["koma"]
users = db["users"]
comics = db["comics"]

def create_user(name, email, username, dob, password_hash , api_cipher):
    return users.insert_one({
        "name": name,
        "email": email,
        "username": username,
        "dob": dob,
        "password_hash": password_hash,
        "api_cipher": api_cipher,
        "created_at": datetime.datetime.utcnow()
    })

def find_user_by_email_or_username(identifier):
    return users.find_one({
        "$or": [{"email": identifier}, {"username": identifier}]
    })

def save_comic(user_id, image_url, panel_prompts, prompt):
    return comics.insert_one({
        "user_id": ObjectId(user_id),
        "image_url": image_url,
        "prompt": prompt,
        "panel_prompts": panel_prompts,
        "likes": [],
        "timestamp": datetime.datetime.utcnow()
    })

def get_user_comics(user_id):
    return list(comics.find({"user_id": ObjectId(user_id)}))

def get_explore_comics():
    return list(comics.find().sort("timestamp", -1))

def get_top_comics():
    return list(comics.find().sort("likes", -1).limit(20))

def like_comic(comic_id, user_id):
    comics.update_one({"_id": ObjectId(comic_id)}, {"$addToSet": {"likes": user_id}})

def get_user_api_key(user_id):
    user = users.find_one({"_id": ObjectId(user_id)})
    if user and "api_cipher" in user:
        return decrypt_api_key(user["api_cipher"])
    return None