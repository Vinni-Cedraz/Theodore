import base64
import logging
from PIL import Image
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

def generate_image(client: OpenAI, memory: str, relationship: str) -> str:
    logging.info(f"memory: {memory}, relationship: {relationship}")
    response = client.images.generate(
        prompt=f"""My {relationship} is having a birthday. Please create 
        an image of some of the elements described in this beautiful memory:
        <memory> {memory} </memory>.""",
        n=1,
        size="1024x1024",
        model="dall-e-3",
        response_format="b64_json"
    )
    return response.data[0].b64_json


def _save_b64_png(b64_str: str, path: str):
    """Save a base64 string as PNG file"""
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64_str))


def insert_generated_images(client: OpenAI, base_image_path: str, memory: str, relationship: str, output_path: str):
    """Insert two 1024x1024 generated images onto large base image"""
    # Generate both images
    bottom_image_b64 = generate_image(client, memory, relationship)
    top_image_b64 = generate_image(client, memory, relationship)
    
    # Save generated images for verification
    _save_b64_png(bottom_image_b64, "static/bottom_image.png")
    _save_b64_png(top_image_b64, "static/top_image.png")
    
    # Open and prepare all images
    base_image = Image.open(base_image_path).convert("RGBA")
    bottom_image = Image.open("static/bottom_image.png").convert("RGBA")
    top_image = Image.open("static/top_image.png").convert("RGBA")
    
    # Calculate positions
    bottom_left_pos = (0, base_image.height - 1024)  # Bottom left
    top_right_pos = (base_image.width - 1024, 0)     # Top right
    
    # Paste images with alpha channel
    base_image.paste(bottom_image, bottom_left_pos, bottom_image)
    base_image.paste(top_image, top_right_pos, top_image)
    
    # Save the final composite image
    base_image.save(output_path, "PNG")