from state import ExtractedClauses, query, ClauseComplianceResult
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from google import genai
from google.genai import types

# from langchain_core.prompts import ChatPromptTemplate

# Initialize the model

# Accessing secrets


if not st.secrets:
    from dotenv import load_dotenv

    load_dotenv()

groq_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
google_api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
# llm = ChatGroq(
#     api_key=groq_key,
#     # model="llama-3.1-8b-instant"
#     # model="llama-3.3-70b-versatile",
#     model="meta-llama/llama-4-scout-17b-16e-instruct",
#     # model="deepseek-r1-distill-llama-70b",
#     # model="mistral-saba-24b",
#     temperature=0,
# )
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite-preview-06-17",
    google_api_key=google_api_key,  # Replace with your API key
    temperature=0.0,
)
client = genai.Client(api_key=google_api_key)

# llm_m = ChatGroq(
#     api_key=groq_key,
#     # model="llama-3.1-8b-instant"
#     # model="llama-3.3-70b-versatile",
#     model="meta-llama/llama-4-maverick-17b-128e-instruct",
#     # model="deepseek-r1-distill-llama-70b",
#     # model="mistral-saba-24b",
#     temperature=0,
# )

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key,  # Replace with your API key
    temperature=0.7,
)
llm_q = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=google_api_key,  # Replace with your API key
    temperature=0.7,
)
extract_clause_llm = llm.with_structured_output(ExtractedClauses)

query_generator_llm = llm_q.with_structured_output(query)

compliance_model = model.with_structured_output(ClauseComplianceResult)

# test_model = llm.with_structured_output(ClauseComplianceResult)
# res = test_model.invoke(
#     """
# You are a contract compliance assistant.

# Your task is to evaluate whether a clause from a contract complies with Nexify Solutions' internal policy guidelines. Nexify Solutions is receiving services from vendors, and the clause is **proposed by the vendor**.

# 🔺 The clause is proposed by the vendor, and Nexify is the recipient of services. You must evaluate the clause **strictly from Nexify Solutions' perspective**.

# Clause:
# ---
# Nexify must pay within 30 days of invoice
# ---

# Internal Policy:
# ---
# 📘 Section 2: Payment Terms
# 2.1 Purpose
# To standardize Nexify Solution's payment processes for vendors, ensuring timely, accurate, and compliant transactions that support financial predictability.

# 2.2 Policy Details

# Payment Schedule (applies to Nexify Solution):
# – Nexify Solution must make payments within 45 days of invoice receipt (Net 45) to maintain vendor goodwill and comply with industry standards.
# – Early payment discount: Nexify may take a 2% discount if payment is made within 10 days, encouraging early payment.
# – Late payment penalty: If Nexify delays beyond 45 days, a 1.5% monthly interest applies on overdue invoices, calculated daily from the due date, with a 5-day grace period to allow for processing delays.
# – Example: A $10,000 invoice unpaid after 45 days by Nexify incurs $150 monthly interest, prorated daily.
# ---

# ---
# Evaluation Rules:
# 1. If the clause adheres to the internal policy, mark it as compliant.
# 2. If the clause does not match the internal policy exactly, evaluate whether it:
#    - Harms Nexify Solutions (e.g., imposes unfavorable terms, increases costs, or reduces rights). If it harms the company, mark it as non-compliant.
#    - Benefits Nexify Solutions (e.g., provides better terms, improves cash flow, or grants additional rights). If it benefits the company, mark it as compliant — even if it deviates from the policy.
# 3. If the internal policy does not provide enough information to evaluate the clause, mark it as compliant by default and set the policy_source to "none".
# 4. Provide a clear explanation of the compliance logic, including the specific policy (if applicable) or the benefit/harm analysis.
# 5. If the clause is non-compliant, suggest a revision to make it compliant or more favorable to Nexify Solutions.

# Respond strictly in JSON format following the structure of this schema:

# - clause_text: The original clause being reviewed
# - policy_source: The name of the internal policy document used
# - reason: A short explanation of whether the clause is compliant
# - compliant: true or false
# - suggested_revision: If not compliant, suggest a revision (or null if compliant)
# """
# )

# print(res)
