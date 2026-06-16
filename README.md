# Skycast AI 🌤️

A multimodal AI weather assistant that provides real-time weather data, 
voice responses, and AI-generated city images.

## Features
- 🌍 Real-time weather via Open-Meteo API (no API key needed)
- 🔊 Voice responses using OpenAI TTS
- 🎨 Anime-style city image generation using gpt-image-1
- 🤖 Tool calling with GPT-4.1-mini

## Setup
1. Clone the repo
2. Run `uv sync` to install dependencies
3. Add your OpenAI API key to a `.env` file:
OPENAI_API_KEY=your_key_here
4. Run `python main.py`

## Tech Stack
- OpenAI API (GPT-4.1-mini, TTS, gpt-image-1)
- Open-Meteo Weather API
- Gradio
- Python

### Author: Krish Makwana