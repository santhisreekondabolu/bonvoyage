from langchain.agents import initialize_agent, Tool
from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEndpoint

# Inbuilt tools
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools.arxiv.tool import ArxivQueryRun

import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

'''import requests

def get_weather(city: str) -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "API key not found. Please set OPENWEATHER_API_KEY in your .env file."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return f"Failed to retrieve weather data for {city}."

    data = response.json()
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"The current weather in {city} is {weather} with a temperature of {temp}°C."'''

# Loading the env variables
load_dotenv()

# Creating the LLM
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(repo_id = repo_id, temperature = 0.7, 
        task="text-generation", 
        model_kwargs={
            "max_length": 500,
            "token": os.getenv('HF_TOKEN')
        }
    )

# Creating tools
search_tool = Tool(
    name="DuckDuckGo Search",
    func=DuckDuckGoSearchRun().run,
    description="Use this tool to perform web searches using DuckDuckGo."
)

wikipedia_tool = Tool(
    name="Wikipedia Search",
    func=WikipediaAPIWrapper().run,
    description="Use this tool to search Wikipedia for information on any topic."
)

arxiv_tool = Tool(
    name="Arxiv Search",
    func=ArxivQueryRun().run,
    description="Use this tool to search academic papers on arXiv. Provide topics, authors, or keywords, one reference is enough."
)
'''weather_tool = Tool(
    name="OpenWeatherMap",
    func=get_weather,
    description="Use this tool to get current weather. Input should be a city name like 'Paris' or 'New York'."
)'''

# create a list of tools, because agent accepts list of tools   
tools_list = [search_tool, wikipedia_tool, arxiv_tool]
'''tools_list = [search_tool, wikipedia_tool, arxiv_tool, weather_tool]'''

#Creating the agent
agent = initialize_agent(tools_list, llm, agent="zero-shot-react-description", verbose=True)

# Inferencing the agent
response = agent.invoke("What are the trending movies of this month?")
print('Response', response)
print('-' * 40)

response = agent.invoke("Who is current president of India?")
print('Response', response)
print('-' * 40)

response = agent.invoke("Which paper introduced the attention mechanism in deep learning?")
print('Response', response)
print('-' * 40)

'''response = agent.invoke("What is the current weather in Kerala, India?")
print('Response', response)
print('-' * 40)'''