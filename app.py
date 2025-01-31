from flask import Flask, request, jsonify
import google.generativeai as genai
import base64
import json

# Configure API Key
genai.configure(api_key="AIzaSyDpzWWAPEnKkshLYL6H-9Din07FZ7AmFO0")  # **REPLACE WITH YOUR ACTUAL API KEY**

# Initialize Flask app
app = Flask(__name__)

# Function to encode image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# Function to determine MIME type
def get_mime_type(filename):
    if filename.lower().endswith(('.png')):
        return "image/png"
    elif filename.lower().endswith(('.jpg', '.jpeg')):
        return "image/jpeg"
    elif filename.lower().endswith('.webp'):
        return "image/webp"
    else:
        return None

# API endpoint for analyzing images
@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        # Get the uploaded image and user prompt
        image_file = request.files.get('image')
        user_prompt = request.form.get('prompt')

        if not image_file or not user_prompt:
            return jsonify({"error": "Image and prompt are required"}), 400

        # Convert image to Base64
        image_data = encode_image(image_file)

        # Determine the MIME type
        mime_type = get_mime_type(image_file.filename)
        if not mime_type:
            return jsonify({"error": "Unsupported image format"}), 400
        # Call the Google Generative AI API
        model = genai.GenerativeModel('gemini-1.5-flash')  # Use the correct model name
        image_obj = {response.text
            "mime_type": mime_type,
            "data": image_data
        }

        # Generate content using the correct method
        response = model.generate_content([user_prompt, image_obj])

        # Return the response
        return jsonify({
            "response": response.text
        }), 200
        
    except Exception as e:
        print(f"An error occurred: {e}")
        error_details = json.loads(e.args[1]) if len(e.args) > 1 and e.args[1] else None
        return jsonify({
            "error": str(e),
            "details": error_details
        }), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)