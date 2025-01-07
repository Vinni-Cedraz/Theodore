import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
from PIL import Image
from io import BytesIO
import requests
from image_tools import resize_with_cropping, generate_image_front, generate_image_body, generate_image_back

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

    # Generate images
    front_image_url = generate_image_front(client, memory)
    body_image_url = generate_image_body(client, memory)
    back_image_url = generate_image_back(client, memory)

    # Resize and save images
    response = requests.get(front_image_url)
    img_front = Image.open(BytesIO(response.content))
    resized_front = resize_with_cropping(img_front, 2814, 5001)
    resized_front.save("static/front_card.jpg", "JPEG")

    response = requests.get(body_image_url)
    img_body = Image.open(BytesIO(response.content))
    resized_body = resize_with_cropping(img_body, 5000, 3334)
    resized_body.save("static/body_card.jpg", "JPEG")

    response = requests.get(back_image_url)
    img_back = Image.open(BytesIO(response.content))
    resized_back = resize_with_cropping(img_back, 2814, 5001)
    resized_back.save("static/back_card.jpg", "JPEG")

    return jsonify({
        "message": f"Happy Birthday, {name}!",
        "frontImageUrl": front_image_url,
        "bodyImageUrl": body_image_url,
        "backImageUrl": back_image_url
    })

if __name__ == '__main__':
    app.run(debug=True)