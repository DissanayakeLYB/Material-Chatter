import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
OpenAI_API_key =os.getenv("OpenAI_API")

from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# instantiate model
llm = ChatOpenAI(
    api_key=OpenAI_API_key,
    model="gpt-3.5-turbo",
    temperature=0.1, 
    max_tokens=500
)

# prompt template
prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in Materials Science and Engineering. Answer the questions accordingly."),
        ("user", "{input}")
])

# LLM Chain
chain = prompt | llm


st.title("MatTalks")

with st.sidebar:
    st.title("Chat History")

prompt = st.chat_input("Enter the message...")

response = chain.invoke({"input" : prompt})

if prompt:
    
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        st.write(response.content)