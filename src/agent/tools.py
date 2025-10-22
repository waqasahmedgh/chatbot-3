from agents.tool import function_tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")

@function_tool
def get_weather(location: str) -> str:
  """
  Fetch the weather for a given location, returning a short description.
  """
  response = requests.get(
      f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}"
  )
  data = response.json()
  # Example logic
  return f"The current weather in {location} is {data['current']['temp_c']}C degree with {data['current']['condition']['text']}."