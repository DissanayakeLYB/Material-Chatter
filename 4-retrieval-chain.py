import os
from dotenv import load_dotenv
# import streamlit as st
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
ChatOpenAI_API_key = os.getenv("OpenAI_API")

def get_documents_from_web(url):
    loader = WebBaseLoader(url)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 20
    )
    splitDocs = splitter.split_documents(docs)

    return splitDocs


""" doc = Document(
    page_content="A perovskite is any material with a crystal structure following the formula ABX3, which was first discovered as the mineral called perovskite, which consists of calcium titanium oxide (CaTiO3)."
) """

def create_db(docs):
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embedding=embedding)
    return vectorstore


def create_chain(vectorstore):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,
        api_key=ChatOpenAI_API_key
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

docs = get_documents_from_web("https://en.wikipedia.org/wiki/Perovskite_(structure)#:~:text=A%20perovskite%20is%20any%20material,titanium%20oxide%20(CaTiO3).")
vectorstore = create_db(docs)
chain = create_chain(vectorstore)

response = chain.invoke({
    "input" : "Is perovskite a crystal structure?",
})

print(response["answer"])
