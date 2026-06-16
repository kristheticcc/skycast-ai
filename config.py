# Imports
import os
from dotenv import load_dotenv
from openai import OpenAI


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