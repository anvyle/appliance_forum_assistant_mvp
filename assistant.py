from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain

def get_assistant():
    vectordb = Chroma(
        persist_directory="./db",
        embedding_function=OpenAIEmbeddings()
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-4o-2024-11-20"),
        retriever=vectordb.as_retriever(),
    )

    return qa_chain
