from RAG import (
    ensemble_retriever_legal_compliance_guidelines,
    ensemble_retriever_procurement_policy,
    ensemble_retriever_vendor_sla_standards,
)
from state import SubState


def procurement_policy_retriever(state: SubState) -> SubState:
    query = state["query"]
    docs = ensemble_retriever_procurement_policy.invoke(query)
    state["relevant_docs"] = []
    state["retrived_docs"] = []
    state["answer"] = []
    return {"retrived_docs": docs or []}


def vendor_sla_standards_retriever(state: SubState) -> SubState:
    query = state["query"]
    docs = ensemble_retriever_vendor_sla_standards.invoke(query)
    state["relevant_docs"] = []
    state["retrived_docs"] = []
    state["answer"] = []
    return {"retrived_docs": docs or []}


def legal_compliance_guidelines_retriever(state: SubState) -> SubState:
    query = state["query"]
    docs = ensemble_retriever_legal_compliance_guidelines.invoke(query)
    state["relevant_docs"] = []
    state["retrived_docs"] = []
    state["answer"] = []
    return {"retrived_docs": docs or []}
