from PIL import Image
from openai import OpenAI

def generate_image_front(client: OpenAI, memory: str) -> str:
    image_prompt_front = f"""
    Generate a .jpg image for the FRONT of a birthday card,
    inspired by: {memory}.
    Use bright colors, keep it cheerful, 
    and include a birthday theme.
    """
    image_response_front = client.images.generate(
        prompt=image_prompt_front,
        n=1,
        size="1024x1024"
    )
    return image_response_front.data[0].url

def generate_image_body(client: OpenAI, memory: str) -> str:
    image_prompt_body = f"""
    Generate a .jpg image for the BODY of a birthday card,
    inspired by: {memory}.
    Use soft colors, keep it elegant, 
    and include a heartfelt message area.
    """
    image_response_body = client.images.generate(
        prompt=image_prompt_body,
        n=1,
        size="1024x1024"
    )
    return image_response_body.data[0].url

def generate_image_back(client: OpenAI, memory: str) -> str:
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