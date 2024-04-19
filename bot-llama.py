import os
from dotenv import load_dotenv
import streamlit as st

from llama_index.llms.llama_api import LlamaAPI

load_dotenv()

api_key = os.getenv("Llama_index_API")

#instantiate model
llm = LlamaAPI(api_key=api_key)


st.title("PDFTalk")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# here ":=" will assign the chat input to prompt and also checks if True
if prompt := st.chat_input("Talk to your PDF..."): 

    # # display response of the assistant
    with st.chat_message("user"):
        st.write(prompt)

    # add assistant's response to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = llm.invoke(prompt)

    # display response of the assistant
    with st.chat_message("assistant"):
        st.write(response.content)

    # add assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.content})

with st.sidebar:
    st.title("Upload a PDF")
    upload_files = st.file_uploader(" ")
