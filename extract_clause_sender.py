from langgraph.constants import Send
from langchain_core.prompts import PromptTemplate
from state import AgentState
import random


def extract_clause_sender(state: AgentState) -> AgentState:
    return [
        Send("extract_clauses", {"contract": contract})
        for contract in state["contract"]
    ]
