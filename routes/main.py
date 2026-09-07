from flask import Blueprint, render_template
from database.supabase_client import supabase

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_internships = []
    stats = {
        'internships_count': 0,
        'companies_count': 0,
        'applications_count': 0
    }
    
    if supabase:
        try:
            # Fetch latest 6 featured internships
            res = supabase.table('internships').select('*, users(name)').order('created_at', desc=True).limit(6).execute()
            if res.data:
                featured_internships = res.data
                
            # Fetch statistics counts
            interns_res = supabase.table('internships').select('id', count='exact').execute()
            users_res = supabase.table('users').select('id', count='exact').eq('role', 'company').execute()
            apps_res = supabase.table('applications').select('id', count='exact').execute()

            stats['internships_count'] = interns_res.count if hasattr(interns_res, 'count') and interns_res.count is not None else len(featured_internships)
            stats['companies_count'] = users_res.count if hasattr(users_res, 'count') and users_res.count is not None else 0
            stats['applications_count'] = apps_res.count if hasattr(apps_res, 'count') and apps_res.count is not None else 0
        except Exception as e:
            print(f"[Main Route Exception] {e}")

    return render_template('index.html', internships=featured_internships, stats=stats)
