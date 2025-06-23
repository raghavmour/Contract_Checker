from langgraph.constants import Send
from langchain_core.prompts import PromptTemplate
from state import AgentState


def ReRanker_Sender(state: AgentState) -> AgentState:
    return [
        Send("SubGraph", {"clause": clause})
        for clause in state["extracted_clauses"]["clauses"][5:15]
    ]
