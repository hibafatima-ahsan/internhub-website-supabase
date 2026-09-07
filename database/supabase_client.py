import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / '.env')

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL != "https://your-supabase-project-id.supabase.co":
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"[Supabase Error] Failed to initialize Supabase client: {e}")
        supabase = None
else:
    print("[Supabase Warning] SUPABASE_URL and SUPABASE_KEY are not properly set in .env file.")

def get_supabase() -> Client:
    """Helper function to access the initialized Supabase client."""
    if supabase is None:
        raise RuntimeError("Supabase client is not initialized. Please configure SUPABASE_URL and SUPABASE_KEY in your environment.")
    return supabase
