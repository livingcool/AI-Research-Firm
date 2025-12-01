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

## 🚀 Deployment Guide (Streamlit Cloud)

Deploying this app so anyone can use it is free and easy with Streamlit Cloud.

### Prerequisites
1.  A [GitHub](https://github.com/) account.
2.  A [Streamlit Cloud](https://share.streamlit.io/) account (connected to GitHub).

### Step 1: Push Code to GitHub
1.  Initialize a git repository (if you haven't already):
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```
2.  Create a new repository on GitHub (e.g., `autonomous-research-firm`).
3.  Link your local repo to GitHub and push:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/autonomous-research-firm.git
    git branch -M main
    git push -u origin main
    ```

### Step 2: Deploy on Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"New app"**.
3.  Select your repository (`autonomous-research-firm`), branch (`main`), and main file (`app.py`).
4.  **CRITICAL:** Click **"Advanced Settings"** before deploying.
5.  Add your secrets in the "Secrets" field:
    ```toml
    GROQ_API_KEY = "your_groq_api_key_here"
    SUPABASE_URL = "your_supabase_url_here"
    SUPABASE_KEY = "your_supabase_key_here"
    ```
6.  Click **"Deploy"**.

### Step 3: Share!
Once deployed, you will get a public URL (e.g., `https://autonomous-research-firm.streamlit.app`). You can share this link with anyone!
