# routes/manga.py
from flask import Blueprint, request, jsonify
from utils.jwt_handler import decode_token
from utils.manga_gen import generate_panel_prompt, generate_images, create_comic_grid
from utils.cloudinary_upload import upload_image
from models.user_schema import save_comic
from models.user_schema import get_user_comics, get_explore_comics, get_top_comics, comics, like_comic
from bson import ObjectId
import uuid
import shutil
import os


manga_bp = Blueprint("manga", __name__)

@manga_bp.route("/generate", methods=["POST"])
def generate():
    token = request.headers.get("Authorization", "").split(" ")[-1]
    payload = decode_token(token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401

    data = request.get_json()
    prompt = data.get("prompt", "")

    panel_prompts = generate_panel_prompt(prompt, payload["user_id"])
    images = generate_images(panel_prompts,payload["user_id"])
    comic_grid = create_comic_grid(images)


    request_id = str(uuid.uuid4())
    output_dir = f"output/{request_id}"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "comic_strip.png")

    comic_grid.save(output_path)

    image_url = upload_image(output_path)
    print(image_url)
    if not image_url:
        return jsonify({"error": "Image upload failed"}), 500
    save_comic(payload["user_id"], image_url, panel_prompts, prompt)

    shutil.rmtree(output_dir)

    return jsonify({
        "message": "Comic generated",
        "image_url": image_url,
        "panel_prompts": panel_prompts
    })

# already defined:
# generate()

@manga_bp.route("/explore", methods=["GET"])
def explore():
    all_comics = get_explore_comics()
    for comic in all_comics:
        comic["_id"] = str(comic["_id"])
        comic["user_id"] = str(comic["user_id"])
        comic["likes"] = len(comic["likes"])
    return jsonify(all_comics)

@manga_bp.route("/top", methods=["GET"])
def top_comics():
    top = get_top_comics()
    for comic in top:
        comic["_id"] = str(comic["_id"])
        comic["user_id"] = str(comic["user_id"])
        comic["likes"] = len(comic["likes"])
    return jsonify(top)

@manga_bp.route("/my-library", methods=["GET"])
def my_library():
    token = request.headers.get("Authorization", "").split(" ")[-1]
    payload = decode_token(token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401

    comics_list = get_user_comics(payload["user_id"])
    for comic in comics_list:
        comic["_id"] = str(comic["_id"])
        comic["user_id"] = str(comic["user_id"])
        comic["likes"] = len(comic["likes"])
    return jsonify(comics_list)

@manga_bp.route("/likes", methods=["GET"])
def liked_by_me():
    token = request.headers.get("Authorization", "").split(" ")[-1]
    payload = decode_token(token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401

    user_id = payload["user_id"]
    liked_comics = comics.find({"likes": user_id})
    results = []
    for comic in liked_comics:
        comic["_id"] = str(comic["_id"])
        comic["user_id"] = str(comic["user_id"])
        comic["likes"] = len(comic["likes"])
        results.append(comic)
    return jsonify(results)

@manga_bp.route("/like/<comic_id>", methods=["POST"])
def like(comic_id):
    token = request.headers.get("Authorization", "").split(" ")[-1]
    payload = decode_token(token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401

    like_comic(comic_id, payload["user_id"])
    return jsonify({"message": "Comic liked."})
