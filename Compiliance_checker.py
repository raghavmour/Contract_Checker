from state import SubState
from langchain.schema import Document
from model import compliance_model


def combine_docs_with_sources(documents: list[Document]) -> str:
    combined = ""
    for doc in documents:
        source = doc.metadata.get("source", "unknown")
        content = doc.page_content.strip()
        combined += f"Source: {source}\nContent:\n{content}\n\n---\n"
    return combined


def Compiliance_checker(state: SubState) -> SubState:
    state["retrived_docs"] = state["retrived_docs"]
    docs = combine_docs_with_sources(state["relevant_docs"])
    text = state["clause"]["text"]
    if not docs.strip():
        return {
            "answer": [
                {
                    "clause_text": text,
                    "policy_source": "none",
                    "reason": "No internal policy guidelines provided to evaluate the clause against, so it is considered compliant by default.",
                    "compliant": True,
                    "suggested_revision": None,
                }
            ]
        }
    prompt = f"""
  You are a contract compliance assistant.

Your task is to evaluate whether a clause from a contract complies with internal policy guidelines.

Clause:
---
{text}
---

Internal Policy:
---
{docs}
---

**Evaluation Guidelines**:
- If the clause is **stricter** than the policy, it is acceptable and should be marked as compliant.
- The clause does **not need to repeat all internal processes** unless contractually required.
- Mark a clause as **non-compliant only if it contradicts, violates, or weakens** internal policy requirements.
- Missing details are acceptable unless their absence introduces a conflict or allows non-compliance.

Respond strictly in JSON format following the structure of this schema:

- clause_text: The original clause being reviewed
- policy_source: The name of the internal policy document used (e.g., "procurement_policy.pdf")
- reason: A short explanation of whether the clause is compliant
- compliant: true or false
- suggested_revision: If not compliant, suggest a revision (or null if compliant)

"""
    compliance_result = compliance_model.invoke(prompt).model_dump()

    return {"answer": [compliance_result]}
