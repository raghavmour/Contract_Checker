import streamlit as st
from dotenv import load_dotenv
import os

from pypdf import PdfReader
from Extract_clause import extract_clauses
from retriever import process_uploaded_files

st.set_page_config(layout="wide")
st.session_state.setdefault("submitted", False)
st.session_state.setdefault("uploaded_files", [])
st.session_state.setdefault("retrievers", [])
from graph import app
from subgraph import sub_graph

# Load environment variables
if st.secrets:
    os.environ["LANGSMITH_TRACING"] = st.secrets["LANGSMITH_TRACING"]
    os.environ["LANGSMITH_ENDPOINT"] = st.secrets["LANGSMITH_ENDPOINT"]
    os.environ["LANGSMITH_API_KEY"] = st.secrets["LANGSMITH_API_KEY"]
    os.environ["LANGSMITH_PROJECT"] = st.secrets["LANGSMITH_PROJECT"]
else:
    load_dotenv()

# Initialize session state
# Placeholder for embedding (replace with your actual embedding model)
# Example: from langchain.embeddings import OpenAIEmbeddings
# embedding = OpenAIEmbeddings()

# Sidebar to display uploaded files
with st.sidebar:
    st.header("Uploaded Files")
    if st.session_state.get("uploaded_files"):
        for file in st.session_state.uploaded_files:
            st.write(f"- 📄 {file.name}")
    else:
        st.write("No files uploaded yet.")

    st.markdown("---")
    st.header("Retrievers")
    if st.session_state.get("retrievers"):
        for retriever in st.session_state.retrievers:
            st.write(f"- 🤖 {retriever.name}")
    else:
        st.write("No retrievers created yet.")

# File upload section
if not st.session_state.submitted:
    st.title("Document Processing App")
    st.header("Upload Documents")
    st.write("Upload one or more PDF documents to process.")

    # File uploader
    uploaded_files = st.file_uploader(
        "Choose PDF files", accept_multiple_files=True, type=["pdf"]
    )

    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        st.write("Uploaded files:")
        for file in uploaded_files:
            st.write(f"- {file.name}")

    if st.button("Submit Documents"):
        if uploaded_files:
            # Process files to create retrievers
            retrievers = process_uploaded_files(uploaded_files)
            st.session_state.retrievers = retrievers
            st.session_state.submitted = True
            st.success("Documents processed successfully!")
        else:
            st.error("Please upload at least one file before submitting.")
else:
    st.title("📄 Contract Clause Intelligence Suite")

    tab1, tab2 = st.tabs(["📌 Clause Compliance Checker", "📑 Clause Extractor"])

    # --- Tab 1: Clause Compliance Checker ---
    with tab1:
        input_method = st.radio(
            "Choose input method:", ("Upload PDF", "Manual Clause Input")
        )

        if input_method == "Upload PDF":
            uploaded_file = st.file_uploader("Upload a contract PDF", type="pdf")

            if uploaded_file:
                reader = PdfReader(uploaded_file)
                total_pages = len(reader.pages)

                # Split pages into 4-page chunks
                chunks = [
                    (i, min(i + 3, total_pages - 1)) for i in range(0, total_pages, 4)
                ]

                contract_text_chunks = []  # List to hold contract text from each chunk

                for start, end in chunks:
                    chunk_text = ""
                    for i in range(start, end + 1):
                        text = reader.pages[i].extract_text()
                        if text:
                            chunk_text += text
                    contract_text_chunks.append(chunk_text)

                # Optional: combine all chunked texts if you still want to send as one document
                full_contract_text = "\n\n".join(contract_text_chunks)

                if not full_contract_text.strip():
                    st.error("Could not extract text from the uploaded PDF.")
                else:
                    # Create state dictionary
                    state = {"contract": contract_text_chunks}

                    # Call your compliance-checking app
                    response = app.invoke(state)
                    data = response["answer"]

                    st.subheader("Clauses Extracted from Contract")
                    st.write(
                        "Number of extracted clauses:",
                        len(response["extracted_clauses"]),
                    )

                    for idx, clause in enumerate(response["extracted_clauses"], 1):
                        st.markdown(f"### {idx}. {clause['clause_type']}")
                        st.markdown(f"> ***{clause['text']}***")
                        st.markdown("---")

                    if len(response["extracted_clauses"]) > 5:
                        st.warning(
                            "As clauses are more than 5, We will randomly select 5 clauses for compliance check."
                        )

                    st.subheader("Clause Compliance Results")
                    # for idx, clause in enumerate(data, 1):
                    #     compliant_icon = "✅" if clause["compliant"] else "❌"
                    #     st.markdown(
                    #         f"### {idx}. {compliant_icon} {clause['clause_title']}"
                    #     )
                    #     st.markdown(f"**Policy Source:** {clause['policy_source']}")
                    #     st.markdown(f"> ***{clause['clause_text']}***")
                    #     st.markdown(f"**Reason:** {clause['reason']}")

                    #     if not clause["compliant"] and clause.get("suggested_revision"):
                    #         st.markdown(
                    #             f"**Suggested Revision:** _{clause['suggested_revision']}_"
                    #         )

                    #     st.markdown("---")
                    for idx, clause in enumerate(data, 1):
                        compliant_icon = "✅" if clause["compliant"] else "❌"
                        st.markdown(
                            f"### {idx}. {compliant_icon} {clause['clause_title']}"
                        )
                        st.markdown(
                            f"**Extracted Clause (from Input):** {clause['clause_text']}"
                        )
                        st.markdown(f"**Reason:** {clause['reason']}")

                        st.markdown("**Clauses:**")
                        for entry in clause["clauses_internal"]:
                            st.markdown(f"> *{entry}*")

                        st.markdown("---")
        else:
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
                    state = {
                        "clause": {
                            "text": clause_text,
                            "clause_type": clause_type,
                            "metadata": {},
                        }
                    }
                    response = sub_graph.invoke(state)
                    data = response["answer"]

                    st.subheader("Clause Compliance Results")
                    st.table(
                        {
                            "Clause Title": [d["clause_title"] for d in data],
                            "Extracted Clause (from Input)": [
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

    # --- Tab 2: Clause Extractor Only ---
    with tab2:
        st.subheader("Upload Contract PDF to Extract Clauses")

        uploaded_file = st.file_uploader(
            "Upload PDF (Clause Extraction Only)", type="pdf", key="extractor"
        )

        if uploaded_file:
            try:
                reader = PdfReader(uploaded_file)
                total_pages = len(reader.pages)
                chunks = [
                    (i, min(i + 3, total_pages - 1)) for i in range(0, total_pages, 4)
                ]
                all_extracted_clauses = []

                for start_page, end_page in chunks:
                    chunk_text = ""
                    for i in range(start_page, end_page + 1):
                        text = reader.pages[i].extract_text()
                        if text:
                            chunk_text += text

                    if chunk_text.strip():
                        state = {"contract": chunk_text}
                        response = extract_clauses(state)
                        extracted = response.get("extracted_clauses", [])

                        for clause in extracted:
                            clause["page_range"] = f"{start_page + 1}-{end_page + 1}"
                            all_extracted_clauses.append(clause)

                if not all_extracted_clauses:
                    st.warning("⚠️ No clauses were extracted from the document.")
                else:
                    st.success(
                        f"✅ {len(all_extracted_clauses)} clauses extracted from {len(chunks)} chunk(s)."
                    )

                    for idx, clause in enumerate(all_extracted_clauses, 1):
                        st.markdown(
                            f"### {idx}. {clause.get('clause_type', 'Unknown')} (Pages: {clause['page_range']})"
                        )
                        st.markdown(f"> ***{clause.get('text', 'No text found.')}***")
                        st.markdown("---")

            except Exception as e:
                st.error(f"🚨 Error while processing the file: {e}")
