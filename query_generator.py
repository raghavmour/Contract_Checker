from model import query_generator_llm

from state import SubState


def generate_relevant_docs_node(state: SubState) -> SubState:
    clause_text = state["clause"]["text"] or None
    # clause_type = state["clause"]["clause_type"] or "general"
    clause_type = state.get("clause", {}).get("clause_type") or "general"

    # Step 1: Generate a search query using LLM
    prompt = f"""
You are a contract compliance assistant.

Your task is to generate a **focused internal search query** that will help retrieve **relevant internal policy documents or guidelines** needed to review the following contract clause for compliance.

Clause Type: {clause_type}

Clause Text:
\"\"\"
{clause_text}
\"\"\"

Return only the search query as a single-line string, with no additional explanation or formatting
"""

    for attempt in range(3):
        try:
            response = query_generator_llm.invoke(prompt)
            query = response.model_dump()
            state["query"] = query["query"]
            state["retrived_docs"] = []
            state["relevant_docs"] = []
            state["answer"] = []
            return state
        except Exception as e:
            print(f"[Retry {attempt + 1}/{3}] Error generating query: {e}")
            if attempt == 3 - 1:
                raise RuntimeError(
                    "Failed to generate query after multiple retries."
                ) from e
