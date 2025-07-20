# utils/manga_gen.py
from utils.encrypt_decrypt import decrypt_api_key
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from models.user_schema import get_user_api_key

def get_genai_client(user_id):
    api_key = get_user_api_key(user_id)
# testing succesfull
    if not api_key:
        raise ValueError("API key not found or decryption failed")
    return genai.Client(api_key=api_key)

def generate_panel_prompt(prompt , user_id):
    client = get_genai_client(user_id)
    system_prompt = (
        "You are a story-based manga scene generator. Given a user prompt, generate six creative and cinematic manga-style panel ideas. "
        "Each panel should begin with 'Manga style panel:' and describe a unique scene from a manga. Return all as one string.\n\n"
        f"User prompt: {prompt}"
    )

    panel_prompts = []
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[system_prompt]
    )

    if hasattr(response, 'text'):
        panels = [p.strip() for p in response.text.split("Manga style panel:") if p.strip()]
        for p in panels:
            panel_prompts.append("Manga style panel: " + p)
    return panel_prompts

def generate_images(panel_prompts, user_id):
    client = get_genai_client(user_id)
    images = []
    for prompt in panel_prompts:
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=[prompt],
            config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
        )
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                image = Image.open(BytesIO(part.inline_data.data))
                images.append(image)
            else:
                print("⚠️ No image data returned for this part:", part)

    return images

def create_comic_grid(images, columns=2):
    width, height = images[0].size
    rows = (len(images) + columns - 1) // columns
    grid_img = Image.new('RGB', (columns * width, rows * height), color=(255, 255, 255))
    for idx, img in enumerate(images):
        img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
        x = (idx % columns) * width
        y = (idx // columns) * height
        grid_img.paste(img_resized, (x, y))
    return grid_img
