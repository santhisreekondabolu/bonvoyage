import os
import pandas as pd
from dotenv import load_dotenv
import ollama
from langchain_ollama.llms import OllamaLLM
 
 
# Load environment variables (optional, if you need other env vars)
load_dotenv()
 
# Set up file paths
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(base_dir, 'catalog.csv')
output_file_path = os.path.join(base_dir, 'output.html')
 
# Read CSV file
df = pd.read_csv(csv_file_path)
csv_content = df.to_string(index=False)
 
# Define the prompt
mymessage = f"Here is the catalog data:\n{csv_content}\n\nMake a list of 6 things to plant this month in Carpinteria, CA from catalog data. Use HTML table format with columns: Name, Catalog_ID, Instructions. Output just the table."
 
# Define the preamble
preamble = "You are a talented and experienced gardener and a helpful assistant to other gardeners, answering questions about products and services for the Hansel and Petal company."
 
# Combine preamble and message for Ollama
full_prompt = f"{preamble}\n\n{mymessage}"
 
# Initialize the LLM
llm = OllamaLLM(model="deepseek-r1:1.5b")
 
# Call Ollama API
response = ollama.chat(
    model="deepseek-r1:1.5b",  # Replace with your preferred Ollama model (e.g., 'mistral', 'llama3')
    messages=[
        {'role': 'user', 'content': full_prompt}
    ]
)
 
# Extract the response text
response_text = response['message']['content']
print(response_text)
# Save the response to output.html
with open(output_file_path, 'w') as file:
    file.write(response_text)
 
print(f"Response saved to {output_file_path}")


