from langchain.schema import Document
from langchain_cohere import CohereRerank
from state import SubState
import os
from dotenv import load_dotenv

import streamlit as st

# Accessing secrets


if not st.secrets:
    from dotenv import load_dotenv

    load_dotenv()

COHERE_API_KEY = st.secrets.get("COHERE_API_KEY") or os.getenv("COHERE_API_KEY")


def Reranker(state: SubState) -> SubState:
    state["relevant_docs"] = []
    state["answer"] = []

    # 1. Initialize reranker
    reranker = CohereRerank(
        model="rerank-english-v3.0",
        cohere_api_key=COHERE_API_KEY,
    )

    # 2. Your query
    # query = state["query"]
    query = state["clause"]["text"]
    # 3. List of documents you want to rerank
    docs = state["retrived_docs"]

    # 4. Rerank using invoke()
    reranked_docs = reranker.rerank(query=query, documents=docs)

    # relevant_docs = [
    #     docs[item["index"]] for item in reranked_docs if item["relevance_score"] > 0.5
    # ]
    # if len(relevant_docs) < 2 and len(reranked_docs) > 0:
    #     # Since reranked_docs is sorted by relevance, take top documents
    #     num_needed = 2 - len(relevant_docs)
    #     top_indices = [item["index"] for item in reranked_docs[:num_needed]]
    #     # Add top documents, avoiding duplicates
    #     relevant_docs.extend(
    #         [docs[i] for i in top_indices if docs[i] not in relevant_docs]
    #     )
    # relevant_docs = relevant_docs[:2]

    # Take top 2 documents
    top_indices = [item["index"] for item in reranked_docs[:2]]
    relevant_docs = [docs[i] for i in top_indices]

    return {"relevant_docs": relevant_docs}


# from typing import List
# from langchain.schema import Document
# from sentence_transformers import CrossEncoder

# import streamlit as st
# from state import SubState


# # Cache model to avoid reloading on each rerun
# @st.cache_resource
# def load_cross_encoder():
#     return CrossEncoder("mixedbread-ai/mxbai-rerank-xsmall-v1")


# model = load_cross_encoder()


# def rerank_with_cross_encoder(
#     query: str, docs: List[Document], top_k: int = 5, threshold: float = 0.4
# ) -> List[Document]:
#     # Get raw text from documents
#     doc_texts = [doc.page_content for doc in docs]

#     # Use CrossEncoder to rank documents
#     results = model.rank(query, doc_texts, return_documents=True, top_k=top_k)

#     # Filter and convert to langchain Documents
#     reranked_docs = [
#         Document(page_content=res["text"], metadata={"score": float(res["score"])})
#         for res in results
#         if res["score"] > threshold
#     ]

#     return reranked_docs


# def Reranker(state: SubState) -> SubState:
#     state["relevant_docs"] = []
#     state["answer"] = []

#     query = state["query"]
#     docs = state["retrived_docs"]

#     # Apply reranker
#     relevant_docs = rerank_with_cross_encoder(query, docs, top_k=10, threshold=0.5)
#     state["relevant_docs"] = relevant_docs

#     return state
