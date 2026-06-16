# Imports
import json
from tools import get_weather, tools
from config import model_main, openai, system_prompt
from media import talker, artist

# handle_tool_calls_and_cities(): Handles calls to the get_weather function, and extracts cities
def handle_tool_calls(message):
    responses = []
    cities = []

    # For multiple tool calls
    for tool_call in message.tool_calls:
        if tool_call.function.name == "get_weather": # If function matches
            arguments = json.loads(tool_call.function.arguments) # To use as a Python dictionary
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