import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
# NEW: Import local embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def build_vector_store(markdown_content: str):
    """
    Takes raw markdown, chunks it, embeds it using LOCAL CPU models, 
    and returns a FAISS vector store.
    """
    print("🧠 Building the paper's brain (running locally on CPU)...")

    # 1. Chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # Smaller chunks work better for local models
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(markdown_content)
    print(f"🧩 Split document into {len(chunks)} chunks.")

    # 2. Embedding (The Sovereign Switch)
    print("⚙️ Loading local embedding model (all-MiniLM-L6-v2)... this takes a moment initially.")
    
    # This downloads a ~80MB model once and runs it on your machine.
    # It generates vectors without sending data to Google.
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create the vector store
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
    print("✅ Vector store built and ready in memory.")
    
    return vectorstore