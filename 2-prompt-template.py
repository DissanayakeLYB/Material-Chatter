import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
OpenAI_API_key =os.getenv("OpenAI_API")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# instantiate model
llm = ChatOpenAI(
    api_key=OpenAI_API_key,
    model="gpt-3.5-turbo",
    temperature=0.8, 
    max_tokens=500
)

# prompt template
prompt = ChatPromptTemplate("tell me a joke about {subject}")

# LLM Chain
chain = prompt | llm


st.title("MatTalks")

with st.sidebar:
    st.title("Chat History")


prompt = st.chat_input("Enter the message...")

response = chain.invoke({"subject" : prompt})

st.write(response)