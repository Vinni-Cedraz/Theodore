from PIL import Image
from openai import OpenAI
from io import BytesIO
import requests

def generate_image(client: OpenAI, memory: str) -> str:
    image_prompt = f"""
    Generate a .jpg image inspired by: {memory}. Do not include any text.
    The image should be elegant and simple and it should not depict the whole memory,
    but rather a symbol or a hint of it without giving it away.
    """
    image_response = client.images.generate(
        prompt=image_prompt,
        n=1,
        size="1024x1024",
        model="dall-e-2"
    )
    return image_response.data[0].url

def create_mask(base_image_path: str, positions: list, size: tuple) -> BytesIO:
    base_image = Image.open(base_image_path).convert("RGBA")
    mask = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
    for position in positions:
        overlay = Image.new("RGBA", size, (255, 255, 255, 255))
        mask.paste(overlay, position)
    byte_stream = BytesIO()
    mask.save(byte_stream, format='PNG')
    byte_stream.seek(0)
    return byte_stream

def overlay_images(client: OpenAI, base_image_path: str, overlay_image_urls: list, positions: list, output_path: str):
    base_image = Image.open(base_image_path).convert("RGBA")
    mask = create_mask(base_image_path, positions, (1024, 1024))

    # Download overlay images
    overlay_images = []
    for url in overlay_image_urls:
        response = requests.get(url)
        overlay_image = Image.open(BytesIO(response.content)).convert("RGBA")
        overlay_images.append(overlay_image)

    # Create a composite image with the overlays
    for overlay_image, position in zip(overlay_images, positions):
        base_image.paste(overlay_image, position, overlay_image)

    # Save the composite image
    byte_stream = BytesIO()
    base_image.save(byte_stream, format='PNG')
    byte_stream.seek(0)

    # Ensure the image is less than 4 MB
    if byte_stream.getbuffer().nbytes >= 4 * 1024 * 1024:
        raise ValueError("The image size exceeds 4 MB")

    # Use DALL-E 2 to edit the image with the mask
    response = client.images.edit(
        model="dall-e-2",
        image=byte_stream,
        mask=mask,
        prompt="A decorated image with elegant and simple symbols inspired by the memory.",
        n=1,
        size="1024x1024"
    )

    # Save the final image
    final_image_url = response.data[0].url
    final_response = requests.get(final_image_url)
    final_image = Image.open(BytesIO(final_response.content))
    final_image.save(output_path, "PNG")