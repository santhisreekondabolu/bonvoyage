import streamlit as st
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import torch

torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]  # To avoid the streamlit error

# Load environment variables
load_dotenv()

# Initialize HuggingFace model for generation
repo_id = "google/gemma-3-1b-it"
llm = HuggingFaceEndpoint(
    repo_id=repo_id, 
    temperature=0.7, 
    task="text-generation", 
    model_kwargs={
        "max_length": 500,
        "token": os.getenv('HF_TOKEN')
    }
)

# Create prompt template
prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    </context>
    Question: {input}
    """
)

def create_vector_embedding():
    if "vectors" not in st.session_state:
        # Using HuggingFace embeddings instead of OpenAI
        st.session_state.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        st.session_state.loader = PyPDFDirectoryLoader("research_papers")  # specify the directory
        st.session_state.docs = st.session_state.loader.load()  # load documents
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:100])  # to avoid delay
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

st.title("RAG Document Q&A with HuggingFace Embeddings")
user_prompt = st.text_input("Enter your query from the research paper")

if st.button("Load docs into vector DB"):
    create_vector_embedding()
    st.write("Vector Database is ready")

import time
if user_prompt:
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    start = time.process_time()
    response = retrieval_chain.invoke({'input': user_prompt})
    print(f"Response time: {time.process_time()-start}")
    st.write(response['answer'])
    with st.expander("References"):
        for i, doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write('------------------------')