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
model_audio = "gpt-4.1-min-tts"
model_image = "gpt-image-1"

# System message to guide assistant's behavior
system_prompt = """
You are skycast, a helpful assistant that gives live weather data given a city using an API. 
You also generate audio for the messages you return, and can generate images of the city as well.
If you do not know the answer, just say so. 
"""

# get_weather(): Returns the weather of a given city using an API
def get_weather():
    return 0

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
    with tempfile.NamedTemporaryFile(suffix = "mp3", delete = False) as f:
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
