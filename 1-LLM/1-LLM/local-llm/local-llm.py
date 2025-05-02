# Import the ChatPromptTemplate class to define how prompts will be formatted
from langchain_core.prompts import ChatPromptTemplate

# Import the OllamaLLM class to use an LLM hosted via the Ollama backend
from langchain_ollama.llms import OllamaLLM

# Import Streamlit for building the web interface
import streamlit as st

# Set the title of the web app
st.title("Langchain-DeepSeek-R1 app")


# Define the prompt template that will be used to format user questions
template = """Question: {question}

Answer: Let's think step by step."""

# Create a prompt object from the template
prompt = ChatPromptTemplate.from_template(template)

# Instantiate the LLM using DeepSeek-R1 model via Ollama
llm = OllamaLLM(model="deepseek-r1:1.5b")

# Create a simple pipeline where the formatted prompt is passed to the model
chain = prompt | llm
# Get user input from a chat-like input box
question = st.chat_input("Enter your question here")

# If the user submitted a question, run the chain and display the response
if question: 
    st.write(chain.invoke({"question": question}))
