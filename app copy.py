from flask import Flask, request, jsonify
import google.generativeai as genai
import base64
import json
import os
from dotenv import load_dotenv
import mimetypes
import logging

# Load environment variables
load_dotenv()

# Configure API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Use environment variable for API key

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/webp"}

# Function to encode image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# Function to determine MIME type
def get_mime_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type

# Function to validate image file
def validate_image_file(image_file):
    if not image_file:
        return False, "No image file provided"
    if image_file.content_length > MAX_FILE_SIZE:
        return False, "File size exceeds the limit (10 MB)"
    mime_type = get_mime_type(image_file.filename)
    if mime_type not in ALLOWED_MIME_TYPES:
        return False, "Unsupported file type"
    return True, None

# API endpoint for analyzing images
@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        # Get the uploaded image and user prompt
        image_file = request.files.get('image')
        user_prompt = request.form.get('prompt')

        # Validate image file
        is_valid, error_message = validate_image_file(image_file)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        if not user_prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Convert image to Base64
        image_data = encode_image(image_file)

        # Determine the MIME type
        mime_type = get_mime_type(image_file.filename)
        if not mime_type:
            return jsonify({"error": "Unsupported image format"}), 400

        # Call the Google Generative AI API
        model = genai.GenerativeModel('gemini-1.5-flash')
        image_obj = {
            "mime_type": mime_type,
            "data": image_data
        }

        response = model.generate_content([user_prompt, image_obj])

        if response.candidates:
            return jsonify({
                "response": response.candidates[0].content
            }), 200
        else:
            return jsonify({"error": "No response from the model"}), 500

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        try:
            error_details = json.loads(e.args[1]) if len(e.args) > 1 and e.args[1] else None
        except json.JSONDecodeError:
            error_details = None
        return jsonify({
            "error": str(e),
            "details": error_details
        }), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "False").lower() == "true")