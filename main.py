# Imports
import json
import os
import requests
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
import tempfile
import base64
from io import BytesIO
from PIL import Image

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

    # Formatting for readability
    current = weather_response["current"]
    return f"Weather for {city}: {current['temperature_2m']}°F, Weather code: {current['weather_code']}, Wind Speed: {current['wind_speed_10m']} mph, Humidity: {current['relative_humidity_2m']}%"

# Description of get_weather function
weather_function = {
    "name": "get_weather",
    "description": "Get the current weather for a given city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city name.",
            }
        },
        "required": ["city"],
        "additionalProperties": False
    }
}


# tools list
tools = [{"type": "function", "function": weather_function}]


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


# handle_tool_calls_and_cities(): Handles calls to the get_weather function, and extracts cities
def handle_tool_calls(message):
    responses = []
    cities = []

    for tool_call in message.tool_calls:
        if tool_call.function.name == "get_weather":
            arguments = json.loads(tool_call.function.arguments)
            city = arguments.get("city")
            cities.append(city)
            weather_details = get_weather(city)
            responses.append(
                {
                    "role":"tool",
                    "content":weather_details,
                    "tool_call_id" : tool_call.id
                }
            )
    return responses, cities

# chat(): Chat function for gradio, maintaining history, performing LLM responses, and calling tools if necessary
def chat(history):
    history = [{"role": h["role"], "content" : h["content"]} for h in history]
    messages = [{"role": "system", "content": system_prompt}] + history

    response = openai.chat.completions.create(
        model = model_main,
        messages = messages,
        tools = tools
    )
    cities = []
    image = None

    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        responses, cities = handle_tool_calls(message)
        messages.append(message)
        messages.extend(responses)
        response = openai.chat.completions.create(
            model = model_main,
            messages = messages,
            tools = tools
        )

    reply = response.choices[0].message.content
    history+=[{"role": "assistant", "content": reply}]
    voice = talker(reply)
    if cities:
        image = artist(cities[0])
    return history, voice, image

# put_message_in_chatbox(): Helper function to add user messages to the chat history
def put_message_in_chatbox(message, history):
    return "", history + [{"role": "user", "content": message}]

# build_ui: Generates the gradio UI for the assistant
def build_ui():
    with gr.Blocks() as ui:
        with gr.Row():
            chatbot = gr.Chatbot(height = 500)
            image_output = gr.Image(height = 500, interactive = False)
        with gr.Row():
            audio_output = gr.Audio(interactive = False, autoplay = True)

        with gr.Row():
            message = gr.Textbox("Chat with skycast!!!")

        message.submit(
                        put_message_in_chatbox,
                        inputs = [message, chatbot],
                        outputs = [message, chatbot]
                ).then(
                        chat,
                        inputs = [chatbot],
                         outputs = [chatbot, audio_output, image_output]
                    )
    return ui

def main():
    ui = build_ui()
    ui.launch()



if __name__ == "__main__":
    main()
