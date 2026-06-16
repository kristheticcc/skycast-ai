# Imports
import requests

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
