from state import AgentState
from model import extract_clause_llm


def extract_clauses(state: AgentState) -> AgentState:
    contract_text = state["contract"]
    prompt = f"""
Extract the following contract clauses from the input:

- Indemnification  
- Warranties and Representations  
- Dispute Resolution  
- Governing Law and Jurisdiction  
- Subcontracting and Assignment  
- Intellectual Property  
- Limitation of Liability  
- Insurance  

For each clause:
- Identify and assign a `clause_type` based on its content (e.g., "Indemnification", "Warranties and Representations", "Dispute Resolution", etc.).
- Provide the clause `text`, limited to **one logical unit of meaning per item**.
- Do not merge unrelated ideas into the same clause, even if they appear in the same paragraph.
- Avoid generic sections, repetitions, and administrative content unless legally relevant.
- Omit headers or section titles unless they contain substantive text.

Return the result as a JSON list of clauses, each with:
- `clause_type`: a short name of the clause type (use one of the types listed above)
- `text`: one clear, focused clause  
Contract:
\"\"\"
{contract_text}
\"\"\"
"""

    for attempt in range(5):
        try:
            extracted = extract_clause_llm.invoke(prompt)
            output = {k: v for k, v in extracted.model_dump().items() if v is not None}
            output["clauses"] = [
                clause
                for clause in output.get("clauses", [])
                if clause.get("text", "").strip()
            ]
            return {
                "extracted_clauses": output["clauses"],
            }
        except Exception as e:
            print(f"[Retry {attempt + 1}/{5}] Error: {e}")
            if attempt == 5 - 1:
                raise RuntimeError(
                    "Failed to extract clauses after multiple retries."
                ) from e


# For each clause:
# - Identify and assign a `clause_type` based on its content (e.g., "Indemnification", "Warranties and Representations", "Dispute Resolution", etc.).
# - Provide the clause `text`, limited to **one logical unit of meaning per item**. If a clause includes multiple conditions, obligations, or concepts, **split them into separate sub-clauses**.
# - Keep each `text` short and self-contained (preferably 1-3 lines).
# - Do not merge unrelated ideas into the same clause, even if they appear in the same paragraph.
# - Avoid generic sections, repetitions, and administrative content unless legally relevant.
# - Omit headers or section titles unless they contain substantive text.


# Extract all legally relevant clauses from the contract text below, strictly adhering to the following clause types as defined in the ExtractedClauses model: indemnification, warranties_and_representations, dispute_resolution, governing_law_and_jurisdiction, subcontracting_and_assignment, intellectual_property, limitation_of_liability, and insurance.

# For each clause:
# - Identify and assign a `clause_type` based on its content (e.g., "Indemnification", "Warranties and Representations", "Dispute Resolution", etc.).
# - Do not merge unrelated ideas into the same clause.
# - Avoid generic sections, repetitions, and administrative content unless legally relevant.
# - Omit headers or section titles unless they contain substantive text.
# - For any clause type where no relevant clause is found, return an empty list.
# - Return a single ExtractedClauses object containing all extracted clauses, formatted as per the ExtractedClauses model.
