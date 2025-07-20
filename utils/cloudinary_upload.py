# utils/cloudinary_upload.py
import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET")
)

def upload_image(image_path):
    try:
        upload_result = cloudinary.uploader.upload(image_path)
        return upload_result.get("secure_url")
    except Exception as e:
        print(f"Cloudinary upload failed: {e}")
        return None

