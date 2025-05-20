import streamlit as st
from assistant import get_assistant
from ingest import prepare_docs, index_documents
from scraper import scrape_threads

st.set_page_config(page_title="Appliance Repair Assistant", page_icon="🔧")

st.title("🔧 Appliance Repair Assistant (MVP)")
st.markdown("""
Welcome to the Appliance Repair Assistant!  
This AI tool allows you to ask questions about appliance issues and get intelligent answers, powered by real repair forum content.

---

### 🧠 What It Does:
1. Scrapes appliance repair forums.
2. Indexes forum threads using vector embeddings.
3. Lets you chat with an AI assistant trained on those threads.

### 🛠️ Tech Stack:
- **Python** – Core backend logic
- **Streamlit** – Web interface
- **BeautifulSoup** – Web scraping
- **LangChain** – Conversational AI with RAG (retrieval augmented generation)
- **OpenAI Embeddings** – Converts text into vector embeddings
- **ChromaDB** – Vector database for semantic search
""")

st.markdown("---")

with st.expander("📥 Crawl and Index New Forum Content"):
    url = st.text_input("Website URL", value="https://appliantology.org/forum/28-site-orientation/")
    num_pages = st.slider("Number of Pages to Scrape", min_value=1, max_value=20, value=1)
    if st.button("Scrape and Index"):
        with st.spinner("Scraping and indexing forum content..."):
            threads = scrape_threads(url, num_pages=num_pages)
            docs = prepare_docs(threads)
            index_documents(docs)
        st.success("Forum content successfully scraped and indexed!")

st.markdown("---")

st.markdown("## 🤖 Chat with the Assistant")

query = st.text_input("Ask a question about an appliance issue:")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if query:
    assistant = get_assistant()
    result = assistant.invoke({"question": query, "chat_history": st.session_state.chat_history})
    st.session_state.chat_history.append((query, result["answer"]))

    st.markdown("### 💡 Answer:")
    st.write(result["answer"])

    with st.expander("🧾 Chat History"):
        for q, a in st.session_state.chat_history:
            st.markdown(f"**You:** {q}")
            st.markdown(f"**Assistant:** {a}")
