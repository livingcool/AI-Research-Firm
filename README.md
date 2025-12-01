# 🧬 Autonomous Research Firm

An AI-powered research engine that combines academic deep dives with real-time market intelligence.

## Features
- **Academic Research**: Search ArXiv, analyze PDFs, and extract visuals.
- **Market Intelligence**: Real-time web search for SWOT analysis and strategic reports.
- **Autonomous Analyst**: Chat with your documents and reports using Llama 3.
- **History**: Save your research reports to Supabase.

## Setup

1.  **Clone the repository**
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Variables**:
    Create a `.env` file or set these in your deployment platform (e.g., Streamlit Cloud Secrets):
    ```
    GROQ_API_KEY=your_groq_key
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key
    ```
4.  **Run Locally**:
    ```bash
    streamlit run app.py
    ```

## Deployment (Streamlit Cloud)

1.  Push this code to a GitHub repository.
2.  Go to [share.streamlit.io](https://share.streamlit.io).
3.  Connect your GitHub and select this repo.
4.  In "Advanced Settings", add your secrets (`GROQ_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`).
5.  Deploy!
