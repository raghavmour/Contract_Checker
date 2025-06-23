import streamlit as st
from dotenv import load_dotenv
import os
from graph import app
from pypdf import PdfReader


load_dotenv()  # Load variables from .env

st.title("Contract Clause Compliance Checker")

# Upload PDF
uploaded_file = st.file_uploader("Upload a contract PDF", type="pdf")

if uploaded_file:
    # Read PDF content using PyPDF
    reader = PdfReader(uploaded_file)
    contract_text = ""
    for page in reader.pages:
        contract_text += page.extract_text() or ""

    # Check if any text was extracted
    if not contract_text.strip():
        st.error("Could not extract text from the uploaded PDF.")
    else:
        # Create state dictionary
        state = {"contract": contract_text}

        # Call your compliance-checking app
        response = app.invoke(state)
        data = response["answer"]

        # Display results in a table
        st.subheader("Clause Compliance Results")
        st.table(
            {
                "Extracted Clause (from Contract)": [d["clause_text"] for d in data],
                "Retrieved From": [d["policy_source"] for d in data],
                "Compliance Logic": [d["reason"] for d in data],
                "Status": [
                    "✅ Compliant" if d["compliant"] else "❌ Non-compliant"
                    for d in data
                ],
                "Suggested Revision": [
                    (
                        d["suggested_revision"]
                        if not d["compliant"] and d["suggested_revision"]
                        else "N/A"
                    )
                    for d in data
                ],
            }
        )
