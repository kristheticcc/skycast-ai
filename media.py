# Imports
import tempfile
import base64
from io import BytesIO
from PIL import Image
from config import model_image, model_audio, openai

# artist(): Generates an image for the given city
def artist(city):
    image_response = openai.images.generate(
        model = model_image,
        prompt = f"An image representing a vacation in city {city}, in an anime art style",
        size = "1024x1024",
        n = 1
    )
    image_base64 = image_response.data[0].b64_json
    image_data = base64.b64decode(image_base64)
    return Image.open(BytesIO(image_data))

# talker(): Generates audio given a message
def talker(message):
    response = openai.audio.speech.create(
        model = model_audio,
        voice = "coral",
        input = message
    )
    with tempfile.NamedTemporaryFile(suffix = ".mp3", delete = False) as f:
        f.write(response.content)
        return f.name


