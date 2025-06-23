from langchain.schema import Document
from langchain_cohere import CohereRerank
from state import SubState
import os
from dotenv import load_dotenv

load_dotenv()


def Reranker(state: SubState) -> SubState:
    state["relevant_docs"] = []
    state["answer"] = []

    # 1. Initialize reranker
    reranker = CohereRerank(
        model="rerank-english-v3.0",
        cohere_api_key=os.getenv("cohere_api_key"),
    )

    # 2. Your query
    query = state["query"]

    # 3. List of documents you want to rerank
    docs = state["retrived_docs"]

    # 4. Rerank using invoke()
    reranked_docs = reranker.rerank(query=query, documents=docs)

    relevant_docs = [
        docs[item["index"]] for item in reranked_docs if item["relevance_score"] > 0.5
    ]

    return {"relevant_docs": relevant_docs}
