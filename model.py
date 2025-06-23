from state import ExtractedClauses, query, ClauseComplianceResult
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import streamlit as st

# Accessing secrets


if not st.secrets:
    from dotenv import load_dotenv

    load_dotenv()

groq_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    api_key=groq_key,
    # model="llama-3.1-8b-instant"
    # model="meta-llama/llama-4-maverick-17b-128e-instruct",
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0,
)

extract_clause_llm = llm.with_structured_output(ExtractedClauses)

query_generator_llm = llm.with_structured_output(query)

compliance_model = llm.with_structured_output(ClauseComplianceResult)
