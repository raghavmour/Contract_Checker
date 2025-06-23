from langchain_cohere import CohereEmbeddings
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain.retrievers.ensemble import EnsembleRetriever

import pickle

import streamlit as st

# Accessing secrets


if not st.secrets:
    from dotenv import load_dotenv

    load_dotenv()

COHERE_API_KEY = st.secrets.get("COHERE_API_KEY ") or os.getenv("COHERE_API_KEY ")

vectordb_path = "faiss_cohere_index_procurement_policy"
splits_path = "splits.pkl_procurement_policy"


# Initialize Cohere embeddings
embedding = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=COHERE_API_KEY,
    user_agent="langchain",
)
# Check if FAISS vector store and splits exist, else build them
if os.path.exists(vectordb_path):
    print("📦 Loading existing FAISS vector store...")
    vectordb = FAISS.load_local(
        vectordb_path, embedding, allow_dangerous_deserialization=True
    )
    if os.path.exists(splits_path):
        print("📄 Loading cached document splits...")
        with open(splits_path, "rb") as f:
            splits = pickle.load(f)
    else:
        print("⚠️ Splits not found, rebuilding...")
        loader = PyPDFLoader(
            "procurement_policy.pdf"
        )  # Replace with your actual file path
        pages = loader.load()
        full_text = "\n".join([page.page_content for page in pages])
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        splits = splitter.create_documents(
            texts=[full_text], metadatas=[{"source": "procurement_policy.pdf"}]
        )

        with open(splits_path, "wb") as f:
            pickle.dump(splits, f)
        print("💾 Document splits saved.")
else:
    print("🔧 Building FAISS vector store...")
    loader = PyPDFLoader("procurement_policy.pdf")  # Replace with your actual file path
    pages = loader.load()
    full_text = "\n".join([page.page_content for page in pages])
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    splits = splitter.create_documents(
        texts=[full_text], metadatas=[{"source": "procurement_policy.pdf"}]
    )

    vectordb = FAISS.from_documents(splits, embedding=embedding)
    vectordb.save_local(vectordb_path)
    with open(splits_path, "wb") as f:
        pickle.dump(splits, f)
    print("💾 Vector store and splits saved.")

# Create FAISS retriever for similarity search
faiss_retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# Create BM25 retriever for keyword search
bm25_retriever = BM25Retriever.from_documents(splits)
bm25_retriever.k = 3

# Combine FAISS and BM25 retrievers into a hybrid retriever
ensemble_retriever_procurement_policy = EnsembleRetriever(
    retrievers=[faiss_retriever, bm25_retriever],
    weights=[0.5, 0.5],  # Equal weighting for similarity and keyword search
)

vectordb_path = "faiss_cohere_index_legal_compliance_guidelines"
splits_path = "splits.pkl_legal_compliance_guidelines"

# Initialize Cohere embeddings
# Check if FAISS vector store and splits exist, else build them
if os.path.exists(vectordb_path):
    print("📦 Loading existing FAISS vector store...")
    vectordb = FAISS.load_local(
        vectordb_path, embedding, allow_dangerous_deserialization=True
    )
    if os.path.exists(splits_path):
        print("📄 Loading cached document splits...")
        with open(splits_path, "rb") as f:
            splits = pickle.load(f)
    else:
        print("⚠️ Splits not found, rebuilding...")
        loader = PyPDFLoader(
            "legal_compliance_guidelines.pdf"
        )  # Replace with your actual file path
        pages = loader.load()
        full_text = "\n".join([page.page_content for page in pages])
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        splits = splitter.create_documents(
            texts=[full_text], metadatas=[{"source": "legal_compliance_guidelines.pdf"}]
        )

        with open(splits_path, "wb") as f:
            pickle.dump(splits, f)
        print("💾 Document splits saved.")
else:
    print("🔧 Building FAISS vector store...")
    loader = PyPDFLoader(
        "legal_compliance_guidelines.pdf"
    )  # Replace with your actual file path
    pages = loader.load()
    full_text = "\n".join([page.page_content for page in pages])
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    splits = splitter.create_documents(
        texts=[full_text], metadatas=[{"source": "legal_compliance_guidelines.pdf"}]
    )

    vectordb = FAISS.from_documents(splits, embedding=embedding)
    vectordb.save_local(vectordb_path)
    with open(splits_path, "wb") as f:
        pickle.dump(splits, f)
    print("💾 Vector store and splits saved.")

# Create FAISS retriever for similarity search
faiss_retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# Create BM25 retriever for keyword search
bm25_retriever = BM25Retriever.from_documents(splits)
bm25_retriever.k = 3

# Combine FAISS and BM25 retrievers into a hybrid retriever
ensemble_retriever_legal_compliance_guidelines = EnsembleRetriever(
    retrievers=[faiss_retriever, bm25_retriever],
    weights=[0.5, 0.5],  # Equal weighting for similarity and keyword search
)

vectordb_path = "faiss_cohere_index_vendor_sla_standards"
splits_path = "splits.pkl_vendor_sla_standards"

# Initialize Cohere embeddings
# Check if FAISS vector store and splits exist, else build them
if os.path.exists(vectordb_path):
    print("📦 Loading existing FAISS vector store...")
    vectordb = FAISS.load_local(
        vectordb_path, embedding, allow_dangerous_deserialization=True
    )
    if os.path.exists(splits_path):
        print("📄 Loading cached document splits...")
        with open(splits_path, "rb") as f:
            splits = pickle.load(f)
    else:
        print("⚠️ Splits not found, rebuilding...")
        loader = PyPDFLoader(
            "vendor_sla_standards.pdf"
        )  # Replace with your actual file path
        pages = loader.load()
        full_text = "\n".join([page.page_content for page in pages])
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        splits = splitter.create_documents(
            texts=[full_text], metadatas=[{"source": "vendor_sla_standards.pdf"}]
        )

        with open(splits_path, "wb") as f:
            pickle.dump(splits, f)
        print("💾 Document splits saved.")
else:
    print("🔧 Building FAISS vector store...")
    loader = PyPDFLoader(
        "vendor_sla_standards.pdf"
    )  # Replace with your actual file path
    pages = loader.load()
    full_text = "\n".join([page.page_content for page in pages])
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    splits = splitter.create_documents(
        texts=[full_text], metadatas=[{"source": "vendor_sla_standards.pdf"}]
    )

    vectordb = FAISS.from_documents(splits, embedding=embedding)
    vectordb.save_local(vectordb_path)
    with open(splits_path, "wb") as f:
        pickle.dump(splits, f)
    print("💾 Vector store and splits saved.")

# Create FAISS retriever for similarity search
faiss_retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# Create BM25 retriever for keyword search
bm25_retriever = BM25Retriever.from_documents(splits)
bm25_retriever.k = 3

# Combine FAISS and BM25 retrievers into a hybrid retriever
ensemble_retriever_vendor_sla_standards = EnsembleRetriever(
    retrievers=[faiss_retriever, bm25_retriever],
    weights=[0.5, 0.5],  # Equal weighting for similarity and keyword search
)
