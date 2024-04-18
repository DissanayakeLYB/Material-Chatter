import os
from dotenv import load_dotenv
import streamlit as st

from llama_index.llms.llama_api import LlamaAPI

load_dotenv()

api_key = os.getenv("Llama_index_API")
llm = LlamaAPI(api_key=api_key)

st.title("MatChat")

prompt = st.chat_input("Enter the message... ")

# chat_history = []

if prompt:

    with st.chat_message("User"):
        st.write(prompt)
    
    # chat_history.append(prompt)

    response = llm.complete(prompt)

    with st.chat_message("Assistant"):
        st.write(response.text)

    # chat_history.append(response)





