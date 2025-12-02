# 🧬 Autonomous Research Firm

**An AI-powered agentic application that automates deep-dive academic research and real-time market intelligence.**

This project leverages Large Language Models (LLMs) to transform hours of manual research into minutes of structured insight. It features a dual-mode engine for handling both static academic papers and dynamic web content, wrapped in a professional, enterprise-grade interface.

---

## 🌟 Key Features

### 🧠 Dual-Mode Intelligence
1.  **Academic Research Mode**:
    *   **PDF Ingestion**: Upload research papers for deep analysis.
    *   **ArXiv Integration**: Search and analyze the latest papers directly from ArXiv.
    *   **Structured Summaries**: Automatically extracts Key Findings, Methodology, and Conclusions.
    *   **RAG (Retrieval-Augmented Generation)**: Chat with the document to ask specific questions.

2.  **Market Intelligence Mode**:
    *   **Real-Time Web Search**: Scours the web for the latest news and articles on any industry or topic.
    *   **Strategic Reports**: Generates Executive Summaries, SWOT Analyses, and Competitor breakdowns.
    *   **Source Citations**: Transparently links to original articles.

### 📊 Dynamic Data Visualization
*   **Auto-Charting**: The AI identifies numerical data within text (e.g., market share, growth rates) and automatically generates interactive **Plotly charts**.
*   **Visual Extraction**: Extracts and displays images/figures from academic PDFs.

### 🛡️ Enterprise-Grade Features
*   **Role-Based Access Control (RBAC)**:
    *   **User Role**: Access to own history and reports.
    *   **Admin Role**: Exclusive dashboard to monitor total API usage, estimated costs, and global research history.
*   **Persistent State**: Session management ensures your reports and charts don't vanish on page refresh.
*   **Feedback System**: Integrated sidebar form for users to rate and comment on the tool, stored in Supabase.

### 📝 Export & Share
*   **One-Click Downloads**: Export any generated report as a professional **PDF** or **Word (DOCX)** document.

---

## 🛠️ Tech Stack Deep Dive

Here is a detailed breakdown of every technology used in this project, explaining **Where** it lives, **How** it works, and **Why** we chose it.

### 1. Streamlit (Frontend & UI)
*   **Where**: `app.py` (The entire user interface).
*   **How**: We used `st.set_page_config` for layout, `st.sidebar` for navigation, `st.tabs` for organizing modes, and `st.markdown` with custom HTML/CSS for the "Premium" dark-mode aesthetic.
*   **Why**: It allows for rapid development of data-driven web apps using pure Python. It handles the frontend-backend connection seamlessly, making it perfect for AI prototypes that need rich interactivity (charts, inputs) without writing React/Vue.

### 2. LangChain (Orchestration)
*   **Where**: `app.py`, `research_tools.py`, `market_tools.py`, `viz_tools.py`.
*   **How**: We used `ChatPromptTemplate` to structure instructions for the AI and `create_stuff_documents_chain` to feed retrieved context (RAG) into the model. It manages the flow of data between the user, the database, and the LLM.
*   **Why**: It provides a standard abstraction layer for working with LLMs. It makes it easy to swap models, manage prompt templates, and build complex "chains" (like RAG) that would be messy to write from scratch.

### 3. Llama 3.3 70B via Groq (Intelligence)
*   **Where**: Instantiated in `app.py` and passed to all tool functions.
*   **How**: Accessed via `ChatGroq` class. We send prompts (e.g., "Analyze this PDF") and receive structured text responses.
*   **Why**:
    *   **Llama 3.3**: A state-of-the-art open-source model with excellent reasoning capabilities, comparable to GPT-4.
    *   **Groq**: An LPU (Language Processing Unit) inference engine that is **blazing fast**. This speed is critical for maintaining a "real-time" feel when generating long reports.

### 4. Supabase (Database & Auth)
*   **Where**: `db_client.py`, `supabase_schema.sql`.
*   **How**:
    *   **Auth**: Handles user signup/login (`supabase.auth`).
    *   **Database**: Stores user profiles, research reports, usage logs, and feedback in PostgreSQL tables.
    *   **RLS**: We wrote SQL policies to ensure users can only see their own data, while Admins can see everything.
*   **Why**: It's an open-source Firebase alternative that gives us a full backend suite: Authentication, a robust PostgreSQL database, and Vector storage (optional) in one platform.

### 5. Plotly (Visualization)
*   **Where**: `viz_tools.py`, `app.py`.
*   **How**: The LLM extracts data into JSON format (e.g., `{"labels": ["A", "B"], "values": [10, 20]}`). We then pass this JSON to `plotly.graph_objects` to render Bar, Pie, or Line charts.
*   **Why**: Unlike static images (Matplotlib), Plotly charts are interactive. Users can hover over data points, zoom in, and toggle series, providing a much more professional user experience.

### 6. FAISS & HuggingFace (RAG Engine)
*   **Where**: `rag_engine.py`, `app.py`.
*   **How**: We use `HuggingFaceEmbeddings` to turn text into numbers (vectors) and `FAISS` to index them. When you ask a question, we find the most similar text chunks to send to the LLM.
*   **Why**: FAISS is a highly efficient library for similarity search. It allows the AI to "read" a 50-page PDF and answer specific questions by only retrieving the relevant pages.

### 7. DuckDuckGo Search (Web Search)
*   **Where**: `market_tools.py`.
*   **How**: We use `DDGS().text()` to programmatically search the web for a given topic and retrieve a list of URLs and snippets.
*   **Why**: It provides a free, privacy-focused API for web search results, allowing our "Market Intelligence" mode to access real-time information without an expensive Google Search API subscription.

### 8. Newspaper3k (Article Scraping)
*   **Where**: `market_tools.py`.
*   **How**: We pass a URL to `Article(url)`, then call `.download()` and `.parse()` to strip away ads, sidebars, and HTML clutter, leaving only the main article text.
*   **Why**: Web pages are messy. Newspaper3k is a battle-tested library for extracting clean text from news sites, ensuring the LLM doesn't get confused by website navigation or ads.

### 9. PyMuPDF4LLM (PDF Parsing)
*   **Where**: `app.py` (`process_pdf` function).
*   **How**: `pymupdf4llm.to_markdown(file_path)` converts the PDF content into Markdown format.
*   **Why**: Standard PDF text extraction often loses structure (headers, lists). This tool preserves the layout as Markdown, which LLMs understand perfectly, leading to much better summaries.

### 10. FPDF & Python-Docx (Export)
*   **Where**: `report_generator.py`.
*   **How**: We programmatically build PDF and Word documents string-by-string, adding headers and formatting.
*   **Why**: Business users need offline copies. These libraries allow us to generate professional-looking files that users can download and share with stakeholders.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   A [Groq](https://console.groq.com/) API Key
*   A [Supabase](https://supabase.com/) Project (URL & Key)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/autonomous-research-firm.git
    cd autonomous-research-firm
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_groq_api_key
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_anon_key
    ```

5.  **Initialize Database**:
    Run the SQL scripts in your Supabase SQL Editor:
    *   `supabase_schema.sql`: Sets up tables (profiles, reports, logs, feedback).
    *   `fix_admin_and_rls.sql`: Sets up RLS policies and Admin role.

### Running the App

```bash
streamlit run app.py
```

---

## 📂 Project Structure

*   `app.py`: Main Streamlit application entry point.
*   `db_client.py`: Handles all Supabase interactions (Auth, Database).
*   `research_tools.py`: Logic for Academic research (ArXiv, PDF processing).
*   `market_tools.py`: Logic for Market research (Web search, Scraping).
*   `viz_tools.py`: AI-powered chart generation logic.
*   `report_generator.py`: PDF and DOCX export functionality.
*   `rag_engine.py`: Vector store and retrieval logic.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
