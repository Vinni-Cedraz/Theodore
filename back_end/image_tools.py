from PIL import Image
from openai import OpenAI

def generate_image_front(client: OpenAI, memory: str) -> tuple:
    image_prompt_front = f"""
    Generate a .jpg image for the FRONT of a birthday card,
    inspired by: {memory}. Do not include any text.
    The image should be elegant and simple and it should not depict the whole memory,
    but rather a symbol or a hint of it without giving it away.
    Remember not to include any text in the image.
    """
    image_response_front = client.images.generate(
        prompt=image_prompt_front,
        n=1,
        size="1024x1024",
        model="dall-e-3"
    )
    front_image_url = image_response_front.data[0].url

    # Ask ChatGPT for the generation ID
    generation_id_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's the generation ID of the last image, (describe only the colors)?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": front_image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    front_generation_id = generation_id_response.choices[0].message.content.strip()

    return front_image_url, front_generation_id

def generate_image_body(client: OpenAI, memory: str, front_generation_id: str) -> tuple:
    image_prompt_body = f"""
    Generate a .jpg image for the BODY of a birthday card,
    inspired by: {memory}. Do not include any text.
    Use a color pallete consistent with generation ID: "{front_generation_id}".
    Remember not to include any text in the image.
    """
    image_response_body = client.images.generate(
        prompt=image_prompt_body,
        n=1,
        size="1024x1024",
        model="dall-e-3"
    )
    body_image_url = image_response_body.data[0].url

    # Ask ChatGPT for the generation ID
    generation_id_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's the generation ID of the last image, (describe only the colors)?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": body_image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    body_generation_id = generation_id_response.choices[0].message.content.strip()

    return body_image_url, body_generation_id

def generate_image_back(client: OpenAI, memory: str, body_generation_id: str) -> str:
    image_prompt_back = f"""
    Generate a .jpg image for the BACK of a birthday card,
    inspired by: {memory}. Do not include any text.
    Use a color pallete consistent with generation ID: "{body_generation_id}".
    This is the back of the card, so it should give a sense of closure or completion, without revealing what's inside.
    Remember not to include any text in the image.
    """
    image_response_back = client.images.generate(
        prompt=image_prompt_back,
        n=1,
        size="1024x1024",
        model="dall-e-3"
    )
    return image_response_back.data[0].url

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