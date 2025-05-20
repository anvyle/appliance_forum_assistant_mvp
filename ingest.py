from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

def prepare_docs(threads):
    docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    for t in threads:
        metadata = {"source": t["url"], "title": t["title"]}
        splits = splitter.split_text(t["content"])
        for chunk in splits:
            docs.append(Document(page_content=chunk, metadata=metadata))
    return docs

def index_documents(docs):
    db = Chroma.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(),
        persist_directory="./db"
    )

if __name__ == "__main__":
    from scraper import scrape_threads
    threads = scrape_threads("https://appliantology.org/forum/28-site-orientation/")
    docs = prepare_docs(threads)
    index_documents(docs)
