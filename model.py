import openai
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.indices.postprocessor import SimilarityPostprocessor
import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms.openai import OpenAI
import streamlit as st
from llama_index.core import Settings

def load_data(path,openai_api_key):
    os.environ['OPENAI_API_KEY'] = openai_api_key

    # Create a custom ServiceContext with the API key
    llm = OpenAI(api_key=openai_api_key)
    Settings.llm = OpenAI(llm=llm)
    PERSIST_DIR = "./storage"
    if not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        documents = SimpleDirectoryReader(path).load_data()
        index = VectorStoreIndex.from_documents(documents, service_context=Settings)
        retriever=VectorIndexRetriever(index=index,similarity_top_k=4)
        # store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context, service_context=Settings)



    query_engine=index.as_query_engine()
    try:
        retriever=VectorIndexRetriever(index=index,similarity_top_k=4)
    except:
        st.write("Error")

    postprocessor=SimilarityPostprocessor(similarity_cutoff=0.80)

    query_engine=RetrieverQueryEngine(retriever=retriever,
                                    node_postprocessors=[postprocessor])
    return query_engine


