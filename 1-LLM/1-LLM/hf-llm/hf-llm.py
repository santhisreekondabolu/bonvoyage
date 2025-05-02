from langchain_huggingface import HuggingFaceEndpoint
import os
# Import Streamlit for building the web interface
import streamlit as st
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from dotenv import load_dotenv
load_dotenv()


# Set the title of the web app
st.title("Itinerary Planner")

st.header("Trip Details")

with st.form("itinerary_form"):
    origin = st.text_input("Starting Location")
    destination = st.text_input("Destination")
    num_days = st.number_input("Number of Days")
    date = st.date_input("Travel Date")
    submit_button = st.form_submit_button("Generate Itinerary")

# Initializing the llm with the correct task parameter
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    temperature=0.7,
    task="text-generation",
    max_new_tokens=1000,
    huggingfacehub_api_token=os.getenv("HF_TOKEN")
)

if submit_button and origin and destination and num_days:
    prompt = f"""
    Create a {int(num_days)}-day travel itinerary from {origin} to {destination}, starting on {date}.

    Format it in markdown with:
    - Bold dates
    - Bullet points for places
    - Section headings for each day

    Include: weather, flights, places to visit, and suggested accommodation.
    """
    try:
        response = llm.invoke(prompt)
        print("LLM Response:", response)

        if response:
            st.subheader("Your AI-Planned Itinerary")
            st.markdown(f"```markdown\n{response}\n```")
        else:
            st.error("No response received from LLM.")

    except Exception as e:
        print("LLM call failed:", str(e))
        st.error(f"LLM call failed: {e}")
    


print('-' * 40)
