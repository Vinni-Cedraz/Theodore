import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
from PIL import Image, ImageOps
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS


# Get the OpenAI API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

def resize_with_cropping(img: Image.Image, new_width: int, new_height: int) -> Image.Image:
    # Crop
    img_ratio = img.width / img.height
    target_ratio = new_width / new_height

    if img_ratio > target_ratio:
        # Crop sides
        new_width_cropped = int(img.height * target_ratio)
        left = (img.width - new_width_cropped) // 2
        right = left + new_width_cropped
        img = img.crop((left, 0, right, img.height))
    else:
        # Crop top/bottom
        new_height_cropped = int(img.width / target_ratio)
        top = (img.height - new_height_cropped) // 2
        bottom = top + new_height_cropped
        img = img.crop((0, top, img.width, bottom))
    return img.resize((new_width, new_height))

@app.route("/generate-card", methods=["POST"])
def generate_card():
    data = request.get_json()
    name = data.get("name")
    relationship = data.get("relationship")
    memory = data.get("memory")

    # Generate message
    message_prompt = f"""
    You are an AI that generates heartfelt birthday messages. 
    Respond directly with the message and no extra content, pleasantries, or fluff. 
    Compose the message using the memory shared by the user, matching the overall mood of the message but in a cheerful way.
    Write a heartfelt birthday message for {name}, who is my {relationship}. Use this memory to compose the message: {memory}.
    """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message_prompt}]
    )
    birthday_message = completion.choices[0].message.content.strip()

    # Generate image
    image_prompt_front = f"""
    Generate a .jpg image for the FRONT of a birthday card, 
    inspired by: {memory}.
    Use pastel colors, keep it sparse for text, 
    and create an innovative design that sparks curiosity 
    without revealing the inside.
    """
    image_response_front = client.images.generate(
        prompt=image_prompt_front,
        n=1,
        size="1024x1024"
    )
    front_image_url = image_response_front.data[0].url

    image_prompt_body = f"""
    Generate a .jpg image for the BODY of a birthday card, 
    inspired by: {memory}.
    Use pastel colors and keep it sparse so that the text stands out.
    """
    image_response_body = client.images.generate(
        prompt=image_prompt_body,
        n=1,
        size="1024x1024"
    )
    body_image_url = image_response_body.data[0].url

    image_prompt_back = f"""
    Generate a .jpg image for the BACK of a birthday card,
    inspired by: {memory}.
    Use pastel colors, keep it sparse, 
    and do something innovative for the back.
    """
    image_response_back = client.images.generate(
        prompt=image_prompt_back,
        n=1,
        size="1024x1024"
    )
    back_image_url = image_response_back.data[0].url

    # Resize and save images
    response = requests.get(front_image_url)
    img_front = Image.open(BytesIO(response.content))
    resized_front = resize_with_cropping(img_front, 2814, 5001)
    resized_front.save("front_card.jpg", "JPEG")

    response = requests.get(body_image_url)
    img_body = Image.open(BytesIO(response.content))
    resized_body = resize_with_cropping(img_body, 5000, 3334)
    resized_body.save("body_card.jpg", "JPEG")

    response = requests.get(back_image_url)
    img_back = Image.open(BytesIO(response.content))
    resized_back = resize_with_cropping(img_back, 2814, 5001)
    resized_back.save("back_card.jpg", "JPEG")

    return jsonify({
        "message": birthday_message, 
        "frontImageUrl": front_image_url,
        "bodyImageUrl": body_image_url,
        "backImageUrl": back_image_url
    })

if __name__ == "__main__":
    app.run(debug=True)