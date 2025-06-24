import streamlit as st
from dotenv import load_dotenv
import os
from graph import app
from pypdf import PdfReader
from subgraph import sub_graph

# Load environment variables
if st.secrets:
    os.environ["LANGSMITH_TRACING"] = st.secrets["LANGSMITH_TRACING"]
    os.environ["LANGSMITH_ENDPOINT"] = st.secrets["LANGSMITH_ENDPOINT"]
    os.environ["LANGSMITH_API_KEY"] = st.secrets["LANGSMITH_API_KEY"]
    os.environ["LANGSMITH_PROJECT"] = st.secrets["LANGSMITH_PROJECT"]
else:
    # Local environment (fallback to dotenv or system env)
    load_dotenv()  # Load variables from .env

st.title("Contract Clause Compliance Checker")

# Option to choose input method
input_method = st.radio("Choose input method:", ("Upload PDF", "Manual Clause Input"))

if input_method == "Upload PDF":
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
                    "Extracted Clause (from Contract)": [
                        d["clause_text"] for d in data
                    ],
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

else:
    # Manual input for clause text and type
    clause_text = st.text_area(
        "Enter Clause Text", placeholder="Paste the clause text here..."
    )
    clause_type = st.text_input(
        "Enter Clause Type",
        placeholder="e.g., Payment Terms, Termination, Confidentiality",
    )

    if st.button("Check Compliance"):
        if not clause_text or not clause_type:
            st.error("Please provide both clause text and clause type.")
        else:
            # Create state dictionary for manual input
            state = {
                "clause": {
                    "text": clause_text,
                    "clause_type": clause_type,
                    "metadata": {},  # Optional metadata can be added here
                }
            }

            # Call your compliance-checking app
            response = sub_graph.invoke(state)
            data = response["answer"]

            # Display results in a table
            st.subheader("Clause Compliance Results")
            st.table(
                {
                    "Extracted Clause (from Input)": [d["clause_text"] for d in data],
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
