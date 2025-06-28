from state import AgentState
from model import extract_clause_llm


def extract_clauses(state: AgentState) -> AgentState:
    contract_text = state["contract"]
    prompt = f"""
Extract all legally relevant clauses from the contract text below.

For each clause:
- Identify and assign a `clause_type` based on its content (e.g., "Indemnification", "Warranties and Representations", "Dispute Resolution", etc.).
- Provide the clause `text`, limited to **one logical unit of meaning per item**. If a clause includes multiple conditions, obligations, or concepts, **split them into separate sub-clauses**.
- Keep each `text` short and self-contained (preferably 1-3 lines).
- Do not merge unrelated ideas into the same clause, even if they appear in the same paragraph.
- Avoid generic sections, repetitions, and administrative content unless legally relevant.
- Omit headers or section titles unless they contain substantive text.



Contract:
\"\"\"
{contract_text}
\"\"\"
"""

    extracted = extract_clause_llm.invoke(prompt)

    output = {k: v for k, v in extracted.model_dump().items() if v is not None}

    flattened_clauses = [clause for clauses in output.values() for clause in clauses]

    state["extracted_clauses"] = flattened_clauses

    return state
