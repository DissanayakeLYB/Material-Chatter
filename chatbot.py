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
    max_tokens=1000
)

chat_history = [

]

# prompt template
prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in Materials Science and Engineering. Answer the questions accordingly."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
])

# LLM Chain
chain = prompt | llm


st.title("MatTalks")

with st.sidebar:
    st.title("Chat History")

prompt = st.chat_input("Enter the message...")



response = chain.invoke({"input" : prompt}, {"chat_history": chat_history})

clear_chat = st.button("Clear Chat")



if prompt:
        
    with st.chat_message("user"):
        st.write(prompt)

    chat_history.append(HumanMessage(content=prompt))

    with st.chat_message("assistant"):
        st.write(response.content)
    
    chat_history.append(AIMessage(content=response))


