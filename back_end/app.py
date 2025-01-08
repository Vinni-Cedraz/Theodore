import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from openai import OpenAI
from io import BytesIO
from image_tools import generate_image, overlay_images

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Get the OpenAI API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

@app.route('/generate-card', methods=['POST'])
def generate_card():
    data = request.get_json()
    name = data.get("name")
    relationship = data.get("relationship")
    memory = data.get("memory")

    # Generate bottom image
    bottom_image_url = generate_image(client, memory)

    # Generate top image
    top_image_url = generate_image(client, memory)

    # Overlay images on body.jpg
    base_image_path = "front_end/assets/images/placeholders/body.jpg"
    overlay_image_urls = [bottom_image_url, top_image_url]
    positions = [(0, 1024), (1024, 0)]
    output_path = "static/body_card.png"
    overlay_images(client, base_image_path, overlay_image_urls, positions, output_path)

    return jsonify({
        "message": f"Happy Birthday, {name}!",
        "bodyImageUrl": request.host_url + "static/body_card.png"
    })

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)