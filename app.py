import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import pymupdf4llm 

# --- Page Config & Premium Styling ---
st.set_page_config(page_title="Autonomous Research Firm", layout="wide", page_icon="🧬")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🧬 Autonomous Research Firm</div>', unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Control Center")
    
    server_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    if server_api_key:
        st.success("✅ API Key Active")
        api_key = server_api_key
    else:
        api_key = st.text_input("Groq API Key:", type="password")
        if not api_key:
            st.warning("⚠️ API Key Required")

    mode = st.radio("Select Operation Mode", ["Academic Research (PDF/ArXiv)", "Market Intelligence (Web)", "Research History"])

# --- Session State ---
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user" not in st.session_state:
    st.session_state.user = None

# --- Helper Functions ---
def process_pdf(uploaded_file):
    with st.spinner("🧠 Ingesting Document..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            markdown_content = pymupdf4llm.to_markdown(tmp_path)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = text_splitter.split_text(markdown_content)
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            return FAISS.from_texts(chunks, embedding=embeddings)
        finally:
            os.remove(tmp_path)

# --- Main Logic ---
if not st.session_state.user:
    st.markdown('<div class="card"><h3>🔐 Login Required</h3><p>Please log in to access the Autonomous Research Firm.</p></div>', unsafe_allow_html=True)
    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])
    
    with tab_login:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Log In"):
            from db_client import sign_in, get_user_role
            user = sign_in(email, password)
            if user:
                st.session_state.user = user
                st.session_state.role = get_user_role(user.user.id)
                st.success(f"Logged in as {st.session_state.role.upper()}!")
                st.rerun()
            else:
                st.error("Login failed. Check credentials.")
                
    with tab_signup:
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")
        if st.button("Sign Up"):
            from db_client import sign_up
            user = sign_up(new_email, new_password)
            if user:
                st.success("Account created! Please log in.")
            else:
                st.error("Signup failed.")

else:
    # Logged In View
    st.sidebar.markdown("---")
    st.sidebar.write(f"👤 **{st.session_state.user.user.email}**")
    st.sidebar.caption(f"Role: {st.session_state.role.upper()}")
    
    if st.sidebar.button("Log Out"):
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()

    if api_key:
        llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.3-70b-versatile")

        # === ADMIN DASHBOARD ===
        if st.session_state.role == 'admin':
            if st.sidebar.checkbox("Admin Dashboard", value=False):
                st.subheader("🛡️ Admin Dashboard")
                from db_client import get_all_usage, get_history
                
                # Stats
                usage_data = get_all_usage()
                total_tokens = sum([u['input_tokens'] + u['output_tokens'] for u in usage_data])
                total_cost_est = (total_tokens / 1_000_000) * 0.50 # Rough estimate
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total API Calls", len(usage_data))
                col2.metric("Total Tokens Processed", f"{total_tokens:,}")
                col3.metric("Est. Cost (Groq)", f"${total_cost_est:.4f}")
                
                st.markdown("### 📋 Recent Activity Log")
                st.dataframe(usage_data)
                
                st.markdown("### 🗄️ Global Research History")
                all_reports = get_history(role='admin')
                for item in all_reports:
                    with st.expander(f"[{item['type']}] {item['topic']} (User: {item.get('user_id', 'Unknown')})"):
                        st.markdown(item['content'])
                
                st.stop() # Stop execution here if in Admin Mode

        # === MODE 1: ACADEMIC RESEARCH ===
        if mode == "Academic Research (PDF/ArXiv)":
            st.subheader("📚 Academic Deep Dive")
            
            tab1, tab2 = st.tabs(["Upload PDF", "Search ArXiv"])
            
            with tab1:
                uploaded_file = st.file_uploader("Upload Research Paper", type="pdf")
                if uploaded_file and st.button("Analyze PDF"):
                    st.session_state.vectorstore = process_pdf(uploaded_file)
                    st.success("Brain Built! Ready for Q&A.")

            with tab2:
                from research_tools import search_arxiv, select_best_paper, fetch_and_parse_rich_arxiv
                topic = st.text_input("Enter Research Topic:")
                if st.button("Start Autonomous Research"):
                    with st.spinner("🔍 Searching & Analyzing..."):
                        papers = search_arxiv(topic)
                        best_paper = select_best_paper(topic, papers, llm)
                        
                        st.markdown(f"### 🏆 Selected: {best_paper['title']}")
                        
                        md_text, image_dir = fetch_and_parse_rich_arxiv(best_paper['id'])
                        
                        # Presentation
                        with st.spinner("💡 Generating Presentation..."):
                            presentation_prompt = (
                                f"Create a structured presentation summary:\n\n{md_text[:10000]}\n\n"
                                "Format as:\n# [Title]\n## Key Findings\n- [Point]\n## Methodology\n- [Point]\n## Conclusion\n- [Point]"
                            )
                            response = llm.invoke(presentation_prompt)
                            presentation = response.content
                            
                            # Log Usage
                            from db_client import log_usage
                            usage = response.response_metadata.get('token_usage', {})
                            log_usage(st.session_state.user.user.id, "llama-3.3-70b", usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0))

                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            st.markdown(presentation)
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Save to DB
                            from db_client import save_report
                            save_report(topic, "Academic", presentation, st.session_state.user.user.id)

                        # Visuals
                        st.subheader("📊 Extracted Visuals")
                        if os.path.exists(image_dir):
                            images = [f for f in os.listdir(image_dir) if f.endswith(".png")]
                            if images:
                                cols = st.columns(3)
                                for i, img_file in enumerate(images):
                                    with cols[i % 3]:
                                        st.image(os.path.join(image_dir, img_file), caption=img_file, use_container_width=True)
                        
                        # Build Brain
                        from rag_engine import build_vector_store
                        st.session_state.vectorstore = build_vector_store(md_text)
                        st.success("Brain Built! Ready for Q&A.")

        # === MODE 2: MARKET INTELLIGENCE ===
        elif mode == "Market Intelligence (Web)":
            st.subheader("🌐 Real-Time Market Analysis")
            from market_tools import search_market, generate_market_report
            from viz_tools import extract_data_for_chart, create_chart
            from report_generator import generate_pdf, generate_docx
            
            topic = st.text_input("Enter Market/Industry:")
            if st.button("Generate Intelligence Report"):
                with st.spinner("🕵️‍♂️ Scouting the Web..."):
                    articles = search_market(topic)
                    if articles:
                        st.write(f"Found {len(articles)} relevant sources.")
                        # Pass user_id for logging
                        report = generate_market_report(topic, articles, llm, st.session_state.user.user.id)
                        
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown(report)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Data Viz
                        with st.spinner("📊 Generating Charts..."):
                            # Pass user_id for logging
                            chart_data = extract_data_for_chart(report, llm, st.session_state.user.user.id)
                            fig = create_chart(chart_data)
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                        
                        # Save to DB
                        from db_client import save_report
                        save_report(topic, "Market", report, st.session_state.user.user.id)
                        
                        # Export
                        col1, col2 = st.columns(2)
                        with col1:
                            pdf_path = generate_pdf(report)
                            with open(pdf_path, "rb") as f:
                                st.download_button("📥 Download PDF", f, file_name=f"{topic}_report.pdf")
                        with col2:
                            docx_path = generate_docx(report)
                            with open(docx_path, "rb") as f:
                                st.download_button("📝 Download Word", f, file_name=f"{topic}_report.docx")

                        # Enable Chat on this report
                        from rag_engine import build_vector_store
                        st.session_state.vectorstore = build_vector_store(report)
                        st.success("Context Loaded! Ask questions about the report.")
                    else:
                        st.error("No articles found.")

        # === MODE 3: HISTORY ===
        elif mode == "Research History":
            st.subheader("🗄️ Intelligence Archives")
            from db_client import get_history
            # Pass role to get_history
            history = get_history(st.session_state.user.user.id, st.session_state.role)
            
            if history:
                for item in history:
                    with st.expander(f"{item['created_at'][:10]} - {item['type']}: {item['topic']}"):
                        st.markdown(item['content'])
            else:
                st.info("No saved reports found.")

        # === CHAT INTERFACE (Global) ===
        if st.session_state.vectorstore:
            st.markdown("---")
            st.subheader("💬 Analyst Chat")
            
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("Ask follow-up questions..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    try:
                        retriever = st.session_state.vectorstore.as_retriever()
                        system_prompt = "You are an expert analyst. Answer based on the provided context."
                        prompt_template = ChatPromptTemplate.from_messages([
                            ("system", system_prompt),
                            ("human", "{input}"),
                        ])
                        chain = create_stuff_documents_chain(llm, prompt_template)
                        rag_chain = create_retrieval_chain(retriever, chain)
                        
                        response = rag_chain.invoke({"input": prompt})
                        st.markdown(response["answer"])
                        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
                    except Exception as e:
                        st.error(f"Error: {e}")

    else:
        st.info("👈 Please enter your Groq API Key to start.")
