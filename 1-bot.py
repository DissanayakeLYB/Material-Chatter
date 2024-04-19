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
    max_tokens=500
    )

# front end
st.title("MatTalks")

prompt = st.chat_input("Enter the message...")

with st.sidebar:
    st.title("Chat History")

if prompt:

    llm_response = llm.invoke(prompt)
    
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        st.write(llm_response.content)
