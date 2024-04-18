import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
OpenAI_API_key =os.getenv("OpenAI_API")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser,CommaSeparatedListOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


# instantiate model
llm = ChatOpenAI(
    api_key=OpenAI_API_key,
    model="gpt-3.5-turbo",
    temperature=0, 
    max_tokens=500
)

#output parser
def call_string_output_parser(prompt,llm):


    # prompt template
    prompt = ChatPromptTemplate.from_messages(        [
            ("system", "You are an expert in Materials Science and Engineering. Answer the questions accordingly."),
            ("human", "{input}")
    ])

    parser = StrOutputParser()

    # LLM Chain
    chain = prompt | llm | parser

    response = chain.invoke({"input" : prompt})

    return response

def call_list_output_parser(prompt,llm):

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Mention synonyms fro {word} in a comma separated list."),
        ("human", "{word}")
    ])

    parser = CommaSeparatedListOutputParser()

    chain = prompt | llm | parser

    output = chain.invoke({
        "word" : prompt
    })

    return output

def call_json_output_parser(prompt,llm):

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract information from the following phrase. \nformatting instructions : {formatting instructions}"),
        ("human", "{phrase}")
    ])

    class Person(BaseModel):
        name : str = Field("the name of the person")
        age : int = Field("the age of the person")


    parser = JsonOutputParser(pydantic_object=Person)

    chain = prompt | llm | parser

    output = chain.invoke({
        "phrase" : "Max is 30 years old.",
        "format_instructions" : parser.get_format_instructions() 
    })

    return output


st.title("MatTalks")

with st.sidebar:
    st.title("Chat History")

prompt = st.chat_input("Enter the message...")

output = call_string_output_parser(prompt,llm)

st.write(output)