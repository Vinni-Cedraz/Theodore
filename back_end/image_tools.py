import logging
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

def generate_image(client: OpenAI, memory: str, relationship: str) -> str:
    """Generate a 1024x1024 image using DALL-E 3."""
    logging.info(f"memory: {memory}, relationship: {relationship}")
    response = client.images.generate(
        prompt=f"""Today is my {relationship}'s birthday. Please create 
        an image of some of the elements described in this beautiful memory:
        <memory> {memory} </memory>.""",
        n=1,
        size="1024x1024",
        model="dall-e-3",
        response_format="b64_json"
    )
    return response.data[0].b64_json

def _save_b64_png(b64_str: str, path: str):
    """Save a base64 string as PNG file."""
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64_str))

def generate_birthday_message(client: OpenAI, name: str, memory: str, relationship: str) -> str:
    """Generate a heartfelt birthday message using GPT-4."""
    prompt = (
        f"You are Theodore, the main character of the movie Her. "
        f"Write a heartfelt birthday message for {name}, inspired by the memory: '{memory}'. "
        f"Mention the relationship ({relationship}) in the message."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": "You are Theodore, the main character of the movie Her."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    message = response.choices[0].message.content.strip()
    logging.info(f"Generated message: {message}")
    return message

def generate_body_card_no_text(client: OpenAI, base_image_path: str, memory: str, relationship: str, output_path: str):
    """
    Generate and save a composite image without text overlays.
    Produces 'body_card_no_text.png'.
    """
    # Generate images
    bottom_image_b64 = generate_image(client, memory, relationship)
    top_image_b64 = generate_image(client, memory, relationship)
    
    # Save images for verification
    _save_b64_png(bottom_image_b64, "static/bottom_image.png")
    _save_b64_png(top_image_b64, "static/top_image.png")
    
    # Open and prepare images
    base_image = Image.open(base_image_path).convert("RGBA")
    bottom_image = Image.open("static/bottom_image.png").convert("RGBA")
    top_image = Image.open("static/top_image.png").convert("RGBA")
    
    # Calculate positions
    bottom_left_pos = (256, base_image.height - 1280)  
    top_right_pos = (base_image.width - 1280, 256)
    
    # Paste images
    base_image.paste(bottom_image, bottom_left_pos, bottom_image)
    base_image.paste(top_image, top_right_pos, top_image)
    
    # Save intermediate image
    base_image.save(output_path, "PNG")

def add_text_to_card(client: OpenAI, input_image_path: str, output_image_path: str, name: str, memory: str, relationship: str):
    """
    Insert a GPT-generated message into an existing image, saving the final result.
    Reads 'body_card_no_text.png' and writes 'body_card.png'.
    """
    # Load the intermediate image
    base_image = Image.open(input_image_path).convert("RGBA")
    
    # Generate birthday message
    message = generate_birthday_message(client, name, memory, relationship)
    
    # Draw text on the image
    draw = ImageDraw.Draw(base_image)
    font = ImageFont.truetype("arial.ttf", 40)  # Adjust font path/size
    text_position = (base_image.width // 2, base_image.height - 200)
    draw.text(text_position, message, font=font, fill="white", anchor="mm")
    
    # Save the final composite image
    base_image.save(output_image_path, "PNG")