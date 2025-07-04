from langgraph.graph import StateGraph, END, START
from retriever import document_retriever
from query_generator import generate_relevant_docs_node
from state import SubState
from Compiliance_checker import Compiliance_checker
from Reranker import Reranker
from dotenv import load_dotenv
import os

import streamlit as st

if not st.secrets:
    from dotenv import load_dotenv

    load_dotenv()
graph_sub = StateGraph(SubState)

graph_sub.add_node("query_generator", generate_relevant_docs_node)
# graph_sub.add_node("procurement_policy_retriver", procurement_policy_retriever)
# graph_sub.add_node("vendor_sla_standards_retriver", vendor_sla_standards_retriever)
# graph_sub.add_node(
#     "legal_compliance_guidelines_retriver", legal_compliance_guidelines_retriever
# )
graph_sub.add_node("document_retriever", document_retriever)
graph_sub.add_node("Reranker", Reranker)
# graph.add_node("ReRanker",ReRanker)
graph_sub.add_node("Compiliance_checker", Compiliance_checker)

graph_sub.add_edge(START, "query_generator")
# graph_sub.add_edge("query_generator", "procurement_policy_retriver")
# graph_sub.add_edge("query_generator", "vendor_sla_standards_retriver")
# graph_sub.add_edge("query_generator", "legal_compliance_guidelines_retriver")
graph_sub.add_edge("query_generator", "document_retriever")
# graph_sub.add_edge("procurement_policy_retriver", "Reranker")
# graph_sub.add_edge("vendor_sla_standards_retriver", "Reranker")
# graph_sub.add_edge("legal_compliance_guidelines_retriver", "Reranker")
graph_sub.add_edge("document_retriever", "Reranker")

# graph.add_conditional_edges(
#     "SenderNode",
#     ReRanker_Sender,
#     {
#         "ReRanker":"ReRanker"
#     }
# )

graph_sub.add_edge("Reranker", "Compiliance_checker")
graph_sub.add_edge("Compiliance_checker", END)

sub_graph = graph_sub.compile()

# from IPython.display import Image, display

# display(Image(sub_graph.get_graph().draw_mermaid_png()))

# state = {
#     "clause": {
#         "text": "Payment is due within thirty (30) days of the invoice date.",
#         "clause_type": "Fees & Payment",
#         "metadata": {"payment_due_days": "30 days"},
#     }
# }


# response = sub_graph.invoke(state)

# print(response["relevant_docs"])
