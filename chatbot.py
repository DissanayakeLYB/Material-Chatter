import os
import streamlit as st

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OpenAI_API_key = os.getenv("OpenAI_API")


#instantiate model
llm = ChatOpenAI(
    api_key=OpenAI_API_key,
    model="gpt-3.5-turbo",
    temperature=0, 
    max_tokens=100
    )


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
    st.button("Process")