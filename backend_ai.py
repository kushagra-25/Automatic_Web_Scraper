import google.generativeai as genai
import base64
import tkinter as tk
from tkinter import filedialog
import json

# Configure API Key
genai.configure(api_key="AIzaSyDpzWWAPEnKkshLYL6H-9Din07FZ7AmFO0")  # **REPLACE WITH YOUR ACTUAL API KEY**

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to select image file (using tkinter, but could be command-line)
def select_image():
    root = tk.Tk()  # Create a tkinter window (it can be hidden)
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.webp")]
    )
    return file_path

# Ask user to select an image
print("Please select an image file.")
image_path = "C:\\Users\\ankit\\Downloads\\20250131_195117.jpg"

if not image_path:
    print("No image selected. Exiting...")
    exit()

# Convert image to Base64
image_data = encode_image(image_path)

# Determine the MIME type based on the file extension
if image_path.lower().endswith(('.png')):
    mime_type = "image/png"
elif image_path.lower().endswith(('.jpg', '.jpeg')):
    mime_type = "image/jpeg"
elif image_path.lower().endswith('.webp'):
    mime_type = "image/webp"
else:
    print("Unsupported image format. Exiting...")
    exit()

# User prompt
user_prompt = input("Enter your question about the image: ")

try:
    model = genai.GenerativeModel('gemini-pro-vision')

    # Create the image object as a dictionary
    image_obj = {
        "mime_type": mime_type,
        "data": image_data
    }

    response = model.generate(
        prompt=user_prompt,
        image=image_obj  # Pass the image dictionary directly
    )

    if response.candidates:
        print("\nGemini's Response:")
        print(response.candidates[0].content)
    else:
        print("No response from the model.")

except Exception as e:
    print(f"An error occurred: {e}")
    try:
        error_details = json.loads(e.args[1]) if len(e.args) > 1 and e.args[1] else None
        if error_details:
           print("Error details:", error_details)
    except json.JSONDecodeError:
        pass
    