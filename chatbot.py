import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
OpenAI_API_key =os.getenv("OpenAI_API")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.prompts import MessagesPlaceholder

# instantiate model
llm = ChatOpenAI(
    api_key=OpenAI_API_key,
    model="gpt-3.5-turbo",
    temperature=0.1, 
    max_tokens=500
)

chat_history = [

]

# prompt template
prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in Materials Science and Engineering. Answer the questions accordingly."),
        ("user", "{input}")
])

# LLM Chain
chain = prompt | llm

msg = {
    "input" : "Hello"
}

response = chain.invoke(msg)

print(response)