from state import AgentState
from model import extract_clause_llm


def extract_clauses(state: AgentState) -> AgentState:
    contract_text = state["contract"]
    prompt = f"""
Extract all legally relevant clauses from the contract text below.

For each clause:
- Identify and assign a `clause_type` (e.g., Payment Terms, Termination, Confidentiality, Governing Law, Dispute Resolution, etc.)
- Provide the clause `text`, limited to **one logical unit of meaning per item**. If a clause includes multiple conditions, obligations, or concepts, **split them into separate sub-clauses**.
- Keep each `text` short and self-contained (preferably 1-3 lines).
- Do not merge unrelated ideas into the same clause, even if they appear in the same paragraph.
- If the clause contains structured elements (dates, durations, monetary amounts, jurisdictions, parties, notice periods, etc.), extract them into a `metadata` field with clear key-value pairs.
- Avoid generic sections, repetitions, and administrative content unless legally relevant.
- Omit headers or section titles unless they contain substantive text.

Return the result as a JSON list of clauses, each with:
- `clause_type`: a short name of the clause type
- `text`: one clear, focused clause
- `metadata`: key-value pairs if applicable



Contract:
\"\"\"
{contract_text}
\"\"\"
"""

    extracted = extract_clause_llm.invoke(prompt)

    output = {k: v for k, v in extracted.model_dump().items() if v is not None}

    state["extracted_clauses"] = output

    return state
