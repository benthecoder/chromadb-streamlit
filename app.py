__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from chromadb_connection import ChromaDBConnection
import pandas as pd

# Default data
documents = [
    "This is document1",
    "This is document2",
    "Hi there",
    "Welcome to ChromaDB",
    "Streamlit is great!",
    "Another example document",
    "More documents here",
    "Python coding",
    "Data Science Rocks!",
]
metadatas = [
    {"source": "notion"},
    {"source": "google-docs"},
    {"source": "slack"},
    {"source": "github"},
    {"source": "reddit"},
    {"source": "stackoverflow"},
    {"source": "medium"},
    {"source": "linkedin"},
    {"source": "twitter"},
]
ids = [f"doc{i+1}" for i in range(len(documents))]

# Create a connection with a default collection
conn = st.experimental_connection(
    "chroma", type=ChromaDBConnection, collection_name="my-collection"
)
# Add the default documents
conn.add_documents(documents=documents, metadatas=metadatas, ids=ids)

# show document
with st.expander("Show documents"):
    st.json(documents)

# Query section
query_text = st.text_input("Enter your query")
n_results = st.slider("Number of results", min_value=1, max_value=10, value=2)

if query_text:
    results = conn.query(query_texts=[query_text], n_results=n_results)
    st.json(results)
