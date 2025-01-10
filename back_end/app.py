import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from openai import OpenAI
from image_tools import generate_body_card_no_text, add_text_to_card

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Get the OpenAI API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

@app.route('/generate-body-card-no-text', methods=['POST'])
def generate_body_card_no_text_route():
    data = request.get_json()
    memory = data.get("memory")
    relationship = data.get("relationship")

    base_image_path = "front_end/assets/images/placeholders/body.png"
    output_path = "static/body_card_no_text.png"

    generate_body_card_no_text(client, base_image_path, memory, relationship, output_path)

    return jsonify({
        "message": "Generated body_card_no_text.png successfully.",
        "imageUrl": request.host_url + "static/body_card_no_text.png"
    })

@app.route('/add-text-to-card', methods=['POST'])
def add_text_to_card_route():
    data = request.get_json()
    name = data.get("name")
    memory = data.get("memory")
    relationship = data.get("relationship")

    input_image_path = "static/body_card_no_text.png"
    output_image_path = "static/body_card.png"

    add_text_to_card(client, input_image_path, output_image_path, name, memory, relationship)

    return jsonify({
        "message": f"Generated body_card.png with message for {name}.",
        "imageUrl": request.host_url + "static/body_card.png"
    })

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)