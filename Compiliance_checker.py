from state import SubState
from langchain.schema import Document
from state import ClauseComplianceResult
from model import client
from google.genai import types
import json


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
                    "clause_title": state["clause"]["clause_type"],
                    "clause_text": text,
                    "policy_source": "none",
                    "reason": "No internal policy guidelines provided to evaluate the clause against, so it is considered compliant by default.",
                    "compliant": True,
                    "clauses_internal": [],
                }
            ]
        }
    prompt = f"""
You are a contract compliance assistant.

Your task is to evaluate whether a clause from a contract complies with Nexify Solutions' internal policy guidelines. Nexify Solutions is receiving services from vendors, and the clause is proposed by the vendor.

🔺 The clause is proposed by the vendor, and Nexify is the recipient of services. You must evaluate the clause strictly from Nexify Solutions' perspective.

Clause:
---
{text}
---

Internal Policy:
---
{docs}
---

Evaluation Rules:

If the clause adheres to the internal policy, mark it as compliant.

if the clause does match but lacks other key points , still mark it as compliant, but give the improvemnt suggested_revison 

If the clause does not match the internal policy exactly, evaluate whether it:

 -Harms Nexify Solutions (e.g., imposes unfavorable terms, increases costs, or reduces rights). If it harms the company, mark it as non-compliant.

 -Benefits Nexify Solutions (e.g., provides better terms, improves cash flow, or grants additional rights). If it benefits the company, mark it as compliant — even if it deviates from the policy.


If the internal policy does not provide enough information to evaluate the clause, mark it as compliant by default and set the policy_source to "NO INTERNAL POLICY FOUND".


If the clause is non-compliant, suggest a revision to make it compliant or more favorable to Nexify Solutions.


Respond strictly in JSON format following the structure of this schema:

- clause_text: The original clause being reviewed
- policy_source: The name of the internal policy document used
- reason: A short explanation of whether the clause is compliant , keep this short and to the point
- compliant: true or false
- give a list of clauses from the internal policies, each with its source formatted as: 'clause text — `source`' which was used to make the decision of complianncy.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            thinking_config=types.ThinkingConfig(thinking_budget=1024),
            response_schema=ClauseComplianceResult,
        ),
    )
    # compliance_result = (
    #     json_obj = json.loads(response.text)
    #     if response is not None
    #     else {
    #         "clause_text": text,
    #         "policy_source": "none",
    #         "reason": "No internal policy guidelines provided to evaluate the clause against, so it is considered compliant by default.",
    #         "compliant": True,
    #         "clauses_internal": [],
    #     }
    # )
    if response is None or not response.text:
        compliance_result = {
            "clause_text": text,
            "policy_source": "none",
            "reason": "No internal policy guidelines provided to evaluate the clause against, so it is considered compliant by default.",
            "compliant": True,
            "clauses_internal": [],
        }
    else:
        compliance_result = json.loads(response.text)
    compliance_result["clause_title"] = state["clause"][
        "clause_type"
    ]  # Ensure clause_text is included
    return {"answer": [compliance_result]}


# - suggested_revision: If not compliant, suggest a revision (or null if compliant) , keep this short and to the point
