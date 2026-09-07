from flask import Blueprint, render_template, redirect, url_for, flash, session
from database.supabase_client import supabase

student_bp = Blueprint('student', __name__)

@student_bp.route('/student/dashboard')
def dashboard():
    if session.get('role') != 'student':
        flash('Unauthorized access. Student portal required.', 'danger')
        return redirect(url_for('auth.login'))

    student_id = session.get('user_id')
    applications = []

    if supabase:
        try:
            res = supabase.table('applications').select('*, internships(*, users(name))').eq('student_id', student_id).order('applied_at', desc=True).execute()
            if res.data:
                applications = res.data
        except Exception as e:
            flash(f'Error loading applications: {str(e)}', 'danger')

    return render_template('student_dashboard.html', applications=applications)
