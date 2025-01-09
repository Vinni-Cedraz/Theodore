import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from openai import OpenAI
from image_tools import insert_generated_images

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
    memory = data.get("memory")
    relationship = data.get("relationship")

    # Base paths
    base_image_path = "front_end/assets/images/placeholders/body.png"
    output_path = "static/body_card.png"

    # Generate and insert images using inpainting
    insert_generated_images(
        client=client,
        base_image_path=base_image_path,
        memory=memory,
        relationship=relationship,
        output_path=output_path
    )

    return jsonify({
        "message": f"Happy Birthday, {name}!",
        "bodyImageUrl": request.host_url + "static/body_card.png"
    })

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)