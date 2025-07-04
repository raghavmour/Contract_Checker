from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import io
import streamlit as st
import os
from langchain_cohere import CohereEmbeddings
from pypdf import PdfReader
from state import SubState

# Accessing secrets


if not st.secrets:
    from dotenv import load_dotenv

    load_dotenv()

COHERE_API_KEY = st.secrets.get("COHERE_API_KEY ") or os.getenv("COHERE_API_KEY ")
retriever_list = []
# Initialize Cohere embeddings
embedding = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=COHERE_API_KEY,
    user_agent="langchain",
)


def process_uploaded_files(uploaded_files):
    """Process a list of uploaded files and return a list of ensemble retrievers."""
    retrievers = []

    for file in uploaded_files:
        # Read file content

        # Create a temporary file-like object for PyPDFLoader

        # Load and process the PDF
        # loader = PyPDFLoader(file)
        reader = PdfReader(file)
        pages = reader.pages
        full_text = "\n".join([page.extract_text() or "" for page in pages])

        # Split the document
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        splits = splitter.create_documents(
            texts=[full_text], metadatas=[{"source": file.name}]
        )

        # Create FAISS vector store
        vectordb = FAISS.from_documents(splits, embedding=embedding)

        # Create FAISS retriever
        faiss_retriever = vectordb.as_retriever(search_kwargs={"k": 3})

        # Create BM25 retriever
        bm25_retriever = BM25Retriever.from_documents(splits)
        bm25_retriever.k = 3

        # Create ensemble retriever with file name
        ensemble_retriever = EnsembleRetriever(
            retrievers=[faiss_retriever, bm25_retriever],
            weights=[0.5, 0.5],
            name=f"retriever_{file.name.replace('.pdf', '')}",  # Name retriever after file
        )

        retrievers.append(ensemble_retriever)
        if ensemble_retriever.name not in [r.name for r in retriever_list]:
            retriever_list.append(ensemble_retriever)

    return retrievers


def deduplicate_retrievers(retriever_list):
    seen_names = set()
    unique_retrievers = []

    for retriever in retriever_list:
        if retriever.name not in seen_names:
            unique_retrievers.append(retriever)
            seen_names.add(retriever.name)

    return unique_retrievers


def document_retriever(state: SubState) -> SubState:
    """Retrieve documents from a list of retrievers and concatenate results."""
    global retriever_list
    query = state["query"]
    retriever_list = deduplicate_retrievers(retriever_list)
    retrievers = retriever_list  # Get list of retrievers from state
    all_docs = []

    # Invoke each retriever and concatenate results
    for retriever in retrievers:
        docs = retriever.invoke(query)
        all_docs.extend(docs or [])

    # Update state
    state["relevant_docs"] = []
    state["retrived_docs"] = all_docs  # Concatenated list of all retrieved documents
    state["answer"] = []

    return {"retrived_docs": all_docs}
