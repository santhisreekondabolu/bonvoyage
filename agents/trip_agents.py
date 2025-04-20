import crewai
from crewai import Agent, LLM
from tools.trip_tools import MyCustomDuckDuckGoTool
from dotenv import load_dotenv
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import streamlit as st

class TripAgents:

    def __init__(self):
        load_dotenv()
        #self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY")    # Uncomment this line, while running locally
        self.hf_api_key = st.secrets["HUGGINGFACE_API_KEY"]   # Uncomment this line, while running on streamlit cloud

        if not self.hf_api_key:
            raise ValueError("HUGGINGFACE_API_KEY is missing. Please set it in your environment variables.")

        # Hugging Face Model ID
        self.model_id = "huggingface/mistralai/Mistral-7B-Instruct-v0.3"
        #self.model_id = "huggingface/HuggingFaceH4/zephyr-7b-beta"

    def local_expert_agent(self):
        return Agent(
            role='Local cultural guide / Researcher',
            goal='Build a deep, insider-style city guide with history, customs, and hidden gems',
            backstory="""You are a seasoned local expert and cultural ambassador known for crafting authentic city guides that blend local flavor, hidden gems, and practical insights.
            You’ve helped thousands of travelers explore cities like a local by sharing cultural tips, little-known places, event calendars, and insider secrets.
            Your knowledge spans from the bustling markets to quiet corners only locals know — and your writing style is warm, clear, and highly informative.
            Your guides are often featured in travel blogs, tourism boards, and personalized concierge services.""",
            tools=[MyCustomDuckDuckGoTool()],
            llm=LLM(model=self.model_id, api_key=self.hf_api_key),
            verbose=True,
            allow_delegation=False,
            max_iter=1,
        )

    def travel_concierge_agent(self):
        return Agent(
            role='Logistician / Trip architect',
            goal="""Create a detailed, day-wise, logistics-friendly travel itinerary""",
            backstory="""You are an award-winning travel planner and logistics expert, specialized in turning travel goals into seamless, detail-rich itineraries.
            You’ve designed hundreds of tailored travel plans for tourists worldwide — combining flights, accommodations, food, sightseeing, and budgets into smooth, stress-free experiences.
            Your strength lies in blending efficiency with delight — always suggesting the best options (with links only for flights and link only for uber, don't add links for any other options!) while optimizing for budget, interest, and time.
            You often work with premium travel companies and AI travel concierge platforms to turn city guides into executable, real-world plans.""",
            tools=[MyCustomDuckDuckGoTool()],
            llm=LLM(model=self.model_id, api_key=self.hf_api_key),
            verbose=True,
            allow_delegation=False,
            max_iter=2,
        )
