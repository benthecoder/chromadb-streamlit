from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

import chromadb
import pandas as pd


class ChromaDBConnection(ExperimentalBaseConnection[chromadb.PersistentClient]):
    """Basic st.experimental_connection implementation for ChromaDB"""

    def _connect(self, **kwargs) -> chromadb.PersistentClient:
        if "collection_name" in kwargs:
            collection_name = kwargs.pop("collection_name")
        else:
            collection_name = self._secrets["collection_name"]
        persist_directory = "db"
        client = chromadb.PersistentClient(path=persist_directory)
        return client.get_or_create_collection(collection_name)

    def add_documents(self, documents: list, metadatas: list, ids: list):
        return self._instance.add(documents=documents, metadatas=metadatas, ids=ids)

    def query(self, query_texts: list, n_results: int = 2, **kwargs) -> dict:
        @cache_data(ttl=kwargs.get("ttl", 3600))
        def _query(query_texts: list, n_results: int = 2, **kwargs) -> dict:
            results = self._instance.query(
                query_texts=query_texts, n_results=n_results, **kwargs
            )
            return results

        return _query(query_texts=query_texts, n_results=n_results, **kwargs)
