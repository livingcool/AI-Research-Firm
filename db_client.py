import os
from supabase import create_client, Client
from datetime import datetime

def get_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        return None
    return create_client(url, key)

def sign_up(email, password):
    supabase = get_supabase_client()
    if not supabase: return None
    try:
        return supabase.auth.sign_up({"email": email, "password": password})
    except Exception as e:
        print(f"❌ Sign Up Error: {e}")
        return None

def sign_in(email, password):
    supabase = get_supabase_client()
    if not supabase: return None
    try:
        return supabase.auth.sign_in_with_password({"email": email, "password": password})
    except Exception as e:
        print(f"❌ Sign In Error: {e}")
        return None

def save_report(topic: str, report_type: str, content: str, user_id: str = None):
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
    if user_id:
        data["user_id"] = user_id
    
    try:
        supabase.table("research_reports").insert(data).execute()
        print("✅ Report saved to Supabase!")
    except Exception as e:
        print(f"❌ Error saving to Supabase: {e}")

def get_history(user_id: str = None):
    """
    Fetches past reports from Supabase.
    """
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        query = supabase.table("research_reports").select("*").order("created_at", desc=True)
        if user_id:
            query = query.eq("user_id", user_id)
        
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"❌ Error fetching history: {e}")
        return []

def log_usage(user_id: str, model: str, input_tokens: int, output_tokens: int):
    """
    Logs token usage to Supabase.
    """
    supabase = get_supabase_client()
    if not supabase: return

    try:
        supabase.table("usage_logs").insert({
            "user_id": user_id,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        }).execute()
        print(f"📊 Usage logged: {input_tokens} in / {output_tokens} out")
    except Exception as e:
        print(f"❌ Error logging usage: {e}")
