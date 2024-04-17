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
    temperature=0, 
    max_tokens=1000
)

# prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert in Materials Science and Engineering. Answer the questions accordingly.")
        ("user", {"input"})
    ]
)

# LLM Chain
chain = prompt | llm

prompt = st.chat_input("Enter the message...")

response = chain.invoke({"input" : prompt})


st.write(response)