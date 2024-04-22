import os
import streamlit as st

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains import create_retrieval_chain

load_dotenv()

OpenAI_API_key = os.getenv("OpenAI_API")


#instantiate model
llm = ChatOpenAI(
    api_key=OpenAI_API_key,
    model="gpt-3.5-turbo",
    temperature=0, 
    max_tokens=100
    )

def create_db(docs):
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embedding=embedding)
    return vectorstore


def create_chain(vectorstore):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,
        api_key= OpenAI_API_key
    )

    prompt = ChatPromptTemplate.from_template("""
    Answer the user's question :
    Context : {context}
    Question : {input}
    """)

    #chain = prompt | llm 

    chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k":2})

    retrieval_chain = create_retrieval_chain(
        retriever, 
        chain
    )
    return chain


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
    upload_files = st.file_uploader(" ", type="pdf")
    st.button("Process")