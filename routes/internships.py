from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.supabase_client import supabase

internships_bp = Blueprint('internships', __name__)

@internships_bp.route('/internships')
def list_internships():
    search_query = request.args.get('q', '').strip()
    location_filter = request.args.get('location', '').strip()
    
    internships = []
    if supabase:
        try:
            query = supabase.table('internships').select('*, users(name)')
            
            if search_query:
                query = query.ilike('title', f'%{search_query}%')
            if location_filter:
                query = query.ilike('location', f'%{location_filter}%')
                
            res = query.order('created_at', desc=True).execute()
            if res.data:
                internships = res.data
        except Exception as e:
            print(f"[Internships List Error] {e}")

    return render_template('internships.html', internships=internships, search_query=search_query, location_filter=location_filter)

@internships_bp.route('/internship/<string:internship_id>')
def detail(internship_id):
    internship = None
    has_applied = False

    if supabase:
        try:
            res = supabase.table('internships').select('*, users(name, email)').eq('id', internship_id).execute()
            if res.data:
                internship = res.data[0]
                
            student_id = session.get('user_id')
            if student_id and session.get('role') == 'student':
                app_res = supabase.table('applications').select('*').eq('internship_id', internship_id).eq('student_id', student_id).execute()
                if app_res.data and len(app_res.data) > 0:
                    has_applied = True
        except Exception as e:
            flash(f'Error fetching internship details: {str(e)}', 'danger')

    if not internship:
        flash('Internship not found or has been removed.', 'warning')
        return redirect(url_for('internships.list_internships'))

    return render_template('internship_detail.html', internship=internship, has_applied=has_applied)

@internships_bp.route('/internship/<string:internship_id>/apply', methods=['POST'])
def apply(internship_id):
    if session.get('role') != 'student':
        flash('Only registered students can apply for internships.', 'danger')
        return redirect(url_for('auth.login'))

    student_id = session.get('user_id')
    if not supabase:
        flash('Database connection unavailable.', 'danger')
        return redirect(url_for('internships.detail', internship_id=internship_id))

    try:
        # Check duplicate application
        existing = supabase.table('applications').select('*').eq('internship_id', internship_id).eq('student_id', student_id).execute()
        if existing.data and len(existing.data) > 0:
            flash('You have already submitted an application for this internship position.', 'warning')
            return redirect(url_for('internships.detail', internship_id=internship_id))

        # Insert application
        supabase.table('applications').insert({
            'internship_id': internship_id,
            'student_id': student_id,
            'status': 'Pending'
        }).execute()

        flash('Your application was successfully submitted!', 'success')
        return redirect(url_for('student.dashboard'))
    except Exception as e:
        flash(f'Error submitting application: {str(e)}', 'danger')
        return redirect(url_for('internships.detail', internship_id=internship_id))
