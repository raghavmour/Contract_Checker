from langgraph.constants import Send
from langchain_core.prompts import PromptTemplate
from state import AgentState
import random


def ReRanker_Sender(state: AgentState) -> AgentState:
    clauses = state["extracted_clauses"]
    selected_clauses = random.sample(
        clauses, min(5, len(clauses))
    )  # Ensure no error if <5
    return [Send("SubGraph", {"clause": clause}) for clause in selected_clauses]
