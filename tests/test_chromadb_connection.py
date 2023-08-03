from chromadb_connection import (
    ChromaDBConnection,
)
import streamlit as st


def test_connection():
    conn = st.experimental_connection(
        "chroma", type=ChromaDBConnection, collection_name="my-collection"
    )
    assert isinstance(conn, ChromaDBConnection)


# more test...
