import requests
from PIL import Image
import io

# Mock AI API URL (replace with actual API endpoint)
AI_API_URL = "https://api.example.com/analyze"

def process_image_and_get_ingredients(image_file):
    # Convert image to bytes (if needed)
    image_bytes = image_file.read()

    # Call AI API to extract ingredients
    response = requests.post(
        AI_API_URL,
        files={"image": image_bytes},
        data={"task": "extract_ingredients"}
    )

    if response.status_code == 200:
        return response.json().get("ingredients", [])
    else:
        raise Exception("Failed to extract ingredients from image")

def get_product_safety_rating(ingredients, product_category):
    # Call AI API to get safety rating
    response = requests.post(
        AI_API_URL,
        json={
            "ingredients": ingredients,
            "category": product_category,
            "task": "get_safety_rating"
        }
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to get safety rating")