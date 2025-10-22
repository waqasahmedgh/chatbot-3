from typing import cast, List
import chainlit as cl
from agents.tool import function_tool
from agent.tools import get_weather
from agent.agent import config
from agents import Agent, RunConfig, Runner
import requests
import os
from dotenv import load_dotenv

load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")

@cl.set_starters  # type: ignore
async def set_starts() -> List[cl.Starter]:
    return [
        cl.Starter(
            label="Greetings",
            message="Hello! What can you help me today?",
        ),
        cl.Starter(
            label="Weather",
            message="Find the weather in Karachi.",
        ),
    ]
 
@function_tool
@cl.step(type="weather tool")
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

@cl.on_chat_start
async def start():

    cl.user_session.set("chat_history", [])

    cl.user_session.set("config", config)
    agent: Agent = Agent(name="Assistant", 
                         instructions="You are a helpful assistant", 
                         )
    agent.tools.append(get_weather)

    cl.user_session.set("agent", agent)

    await cl.Message(content="Welcome to the Panaversity AI Assistant! How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):

    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    history = cl.user_session.get("chat_history") or []
    
    history.append({"role": "user", "content": message.content})
    
    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_sync(agent, history, run_config=config)
        
        response_content = result.final_output
        
        msg.content = response_content
        await msg.update()

        history.append({"role": "user", "content": response_content})
    
        cl.user_session.set("chat_history", history)
        
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")