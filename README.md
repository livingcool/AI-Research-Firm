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
    *   **Source Citations**: transparently links to original articles.

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

## 🛠️ Tech Stack

*   **Frontend**: [Streamlit](https://streamlit.io/) (Python-based UI)
*   **LLM Orchestration**: [LangChain](https://www.langchain.com/)
*   **Model**: Llama 3.3 70B (via [Groq](https://groq.com/) API for blazing speed)
*   **Database & Auth**: [Supabase](https://supabase.com/) (PostgreSQL + Auth)
*   **Vector Store**: FAISS (Local) / Supabase Vector (Optional)
*   **Visualization**: Plotly
*   **Tools**: `pymupdf4llm` (PDF parsing), `duckduckgo-search` (Web search), `newspaper3k` (Article scraping)

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
