from state import ExtractedClauses, query, ClauseComplianceResult
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    # model="llama-3.1-8b-instant"
    # model="meta-llama/llama-4-maverick-17b-128e-instruct",
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0,
)

extract_clause_llm = llm.with_structured_output(ExtractedClauses)

query_generator_llm = llm.with_structured_output(query)

compliance_model = llm.with_structured_output(ClauseComplianceResult)
