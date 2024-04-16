import os
from dotenv import load_dotenv
import streamlit as st

from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
import pinecone
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
from langchain import HuggingFacePipeline
from huggingface_hub import notebook_login 
import torch

load_dotenv()

OpenAI_API_key = os.getenv("OpenAI_API")

# Front-End
st.title("Material-Chatter")

prompt = st.chat_input("Talk with the MSE expert...")

# chat history
chat_history = []

# response 
if prompt:

    chat_history.append(prompt)

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        st.write(prompt)

with st.sidebar:
    st.title("Chat History")
    for chat in chat_history:
        st.button(chat[:10])




# Back-End

# loading data
URLs = [
    "https://www.udemy.com/"
]

loader = UnstructuredURLLoader(urls = URLs)
data = loader.load()


#chunks
text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200)
text_chunks = text_splitter.split_documents(data)


#embedding model
embeddings = HuggingFaceEmbeddings(model_name='sentence-trasnformers/all-MiniLM-L6-v2')

Pinecone_API_key = os.getenv("pinecone_API")
Pinecone_index = os.getenv("pinecone_index")





