from flask import Blueprint, request, jsonify
from app.services import process_image_and_get_ingredients, get_product_safety_rating

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/upload', methods=['POST'])
def upload_image():
    # Get the uploaded image and product category
    image_file = request.files.get('image')
    product_category = request.form.get('category')

    if not image_file or not product_category:
        return jsonify({"error": "Image and category are required"}), 400

    # Process the image and get ingredients
    ingredients = process_image_and_get_ingredients(image_file)

    # Get safety rating and hazards
    safety_data = get_product_safety_rating(ingredients, product_category)

    return jsonify(safety_data), 200