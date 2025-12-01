import os
from supabase import create_client, Client
from datetime import datetime

def get_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        return None
    return create_client(url, key)

def save_report(topic: str, report_type: str, content: str):
    """
    Saves the generated report to Supabase.
    """
    supabase = get_supabase_client()
    if not supabase:
        print("⚠️ Supabase credentials not found. Report not saved.")
        return

    data = {
        "topic": topic,
        "type": report_type,
        "content": content,
        "created_at": datetime.utcnow().isoformat()
    }
    
    try:
        supabase.table("research_reports").insert(data).execute()
        print("✅ Report saved to Supabase!")
    except Exception as e:
        print(f"❌ Error saving to Supabase: {e}")

def get_history():
    """
    Fetches past reports from Supabase.
    """
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        response = supabase.table("research_reports").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"❌ Error fetching history: {e}")
        return []
