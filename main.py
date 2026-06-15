# Imports
import os
import requests
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
import tempfile

# Load environment variables
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found.")

# Openai client initialization
openai = OpenAI()
model_main = "gpt-4.1-mini"
model_audio = "gpt-4o-mini-tts"
model_image = "gpt-image-1"

# System message to guide assistant's behavior
system_prompt = """
You are skycast, a helpful assistant that gives live weather data given a city using an API. 
You also generate audio for the messages you return, and can generate images of the city as well.
If you do not know the answer, just say so. 
"""

# get_weather(): Returns the weather of a given city using an API
def get_weather(city):

    # step 1: City name -> coordinates

    # Building the url for geocoding API to get the latitude and longitude of the city
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    # HTTP get request to the url
    geo_response = requests.get(geo_url).json()

    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]

    # step 2: Coordinates -> weather
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m&temperature_unit=fahrenheit"
    weather_response = requests.get(weather_url).json()
    return weather_response


# artist(): Generates an image for the given city
def artist(city):
    return 0

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


# handle_tool_calls(): Handles calls to the get_weather function
def handle_tool_calls():
    return 0

# chat(): Chat function for gradio, maintaining history, performing LLM responses, and calling tools if necessary
def chat(message, history):
    return 0

# build_ui: Generates the gradio UI for the assistant
def build_ui():
    return 0

def main():
    print("Hello from skycast-ai!")


if __name__ == "__main__":
    main()
