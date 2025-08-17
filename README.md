# 📄 Contract Clause Intelligence Suite

A Streamlit-powered web application that leverages Large Language Models (LLMs) to analyze legal contracts. This tool can automatically extract clauses from a contract and check them for compliance against a set of user-provided policy documents.

<!-- Add a GIF or screenshot of the application in action here -->
<!-- Example: ![App Demo](link_to_your_demo_gif.gif) -->

---

## ✨ Features

* **Dynamic Knowledge Base**: Upload your internal policy documents, legal guidelines, or standard contract templates to create a customized knowledge base.
* **Automated Clause Extraction**: Upload a contract in PDF format, and the application will automatically identify and extract all its constituent clauses.
* **Comprehensive Compliance Checking**: The application compares extracted clauses against your knowledge base to determine compliance.
    * **✅ Compliant**: The clause aligns with your internal policies.
    * **❌ Non-Compliant**: The clause deviates from your policies.
* **Detailed Feedback**: For each clause, the tool provides:
    * A clear compliance status.
    * The reasoning behind the decision, citing the relevant policy clauses.
    * A suggested revision for non-compliant clauses to bring them into alignment.
* **Dual Input Modes**: Check an entire contract by uploading a PDF or perform a quick check on a single, manually pasted clause.
* **Efficient Document Handling**: Long documents are automatically chunked and processed to fit within model context windows and ensure thorough analysis.

---

## ⚙️ How It Works / Architecture

This application is built on a modern stack for AI-powered document analysis, primarily using a **Retrieval-Augmented Generation (RAG)** architecture.

1.  **Frontend**: The user interface is built with **Streamlit**, providing an interactive and easy-to-use experience for file uploads and results visualization.
2.  **Document Processing**: When you upload your initial "policy" documents, the `retriever.py` module processes them. It splits the documents into smaller chunks, generates embeddings (numerical representations), and stores them in a vector database. This creates a searchable knowledge base (the "Retriever").
3.  **Core Logic (AI Graph)**: The main analysis is orchestrated by **LangGraph**, a framework for building stateful, multi-step AI agents.
    * **Clause Extraction**: When a new contract is uploaded, an LLM call is made via `Extract_clause.py` to identify and parse individual clauses from the raw text.
    * **Compliance Analysis**: For each extracted clause, the system retrieves the most relevant clauses from your policy knowledge base, compares them, and generates a final judgment on compliance, a reason, and a suggested revision if necessary.
4.  **Backend Services**:
    * **LLMs**: The application relies on powerful Large Language Models from providers like **Groq**, **Cohere**, and **Google**.
    * **LangSmith**: The application is configured to use LangSmith for tracing and debugging the complex LLM chains and graphs, ensuring reliability and transparency.

---

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/raghavmour/Contract_Checker.git
cd Contract_Checker
```

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

The repository includes a `requirements.txt` file with all necessary libraries. Install them using pip:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

This application is designed to use Streamlit's secrets management.

**For Local Development:**
1. Create a directory named `.streamlit` in the root of your project.
2. Inside the `.streamlit` directory, create a file named `secrets.toml`.
3. Copy the content below into the file and **replace the placeholder values with your own API keys**.

**`.streamlit/secrets.toml`**:
```toml
# LangSmith Configuration (Optional but Recommended)
LANGSMITH_TRACING = "true"
LANGSMITH_ENDPOINT = "[https://api.smith.langchain.com](https://api.smith.langchain.com)"
LANGSMITH_API_KEY = "your_langsmith_api_key_here"
LANGSMITH_PROJECT = "your_project_name_here"

# LLM Provider API Keys
GROQ_API_KEY = "your_groq_api_key_here"
COHERE_API_KEY = "your_cohere_api_key_here"
GOOGLE_API_KEY = "your_google_api_key_here"
```

**For Streamlit Cloud Deployment:**
When you deploy your app, you will add these same secrets in your app's settings on the Streamlit Community Cloud dashboard. The app code is already set up to read them from there.

**Security Note**: Never commit your `secrets.toml` file to version control. Ensure that `.streamlit/secrets.toml` is listed in your `.gitignore` file.

### 5. Run the Application

Once the setup is complete, run the Streamlit app with the following command:

```bash
streamlit run app.py
```

The application should now be running and accessible in your web browser!

---

## 📖 Usage Guide

The application operates in a simple, two-stage process.

### Stage 1: Upload Policy Documents

1.  When you first launch the app, you will see the **"Document Processing App"** page.
2.  Click the **"Choose PDF files"** button to upload one or more PDF files that constitute your knowledge base (e.g., internal compliance guidelines, standard legal playbooks).
3.  Once the files are selected, click the **"Submit Documents"** button. The system will process these files and create the retrievers.

### Stage 2: Analyze Contracts

After submitting the policy documents, you will be taken to the **"Contract Clause Intelligence Suite"** with two main tabs.

#### Tab 1: Clause Compliance Checker

You have two options here:

* **Upload a PDF**:
    1.  Select the **"Upload PDF"** option.
    2.  Upload the contract you want to analyze.
    3.  The application will automatically extract clauses and display the compliance results.

* **Manual Clause Input**:
    1.  Select the **"Manual Clause Input"** option.
    2.  Paste a single clause into the "Enter Clause Text" area and provide its type.
    3.  Click **"Check Compliance"** to get an instant analysis.

#### Tab 2: Clause Extractor

This tab provides a simpler utility if you only need to extract clauses.

1.  Upload a contract PDF.
2.  The application will process the document and display all the clauses it finds, along with the page range where each clause was located.

