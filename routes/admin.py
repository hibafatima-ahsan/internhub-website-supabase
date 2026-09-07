from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.supabase_client import supabase

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
def dashboard():
    if session.get('role') != 'admin':
        flash('Unauthorized access. Admin privileges required.', 'danger')
        return redirect(url_for('auth.login'))

    users = []
    internships = []
    stats = {'total_users': 0, 'students': 0, 'companies': 0, 'internships': 0, 'applications': 0}

    if supabase:
        try:
            users_res = supabase.table('users').select('*').order('created_at', desc=True).execute()
            if users_res.data:
                users = users_res.data
                stats['total_users'] = len(users)
                stats['students'] = sum(1 for u in users if u.get('role') == 'student')
                stats['companies'] = sum(1 for u in users if u.get('role') == 'company')

            interns_res = supabase.table('internships').select('*, users(name)').order('created_at', desc=True).execute()
            if interns_res.data:
                internships = interns_res.data
                stats['internships'] = len(internships)

            apps_res = supabase.table('applications').select('id', count='exact').execute()
            stats['applications'] = apps_res.count if hasattr(apps_res, 'count') and apps_res.count is not None else 0
        except Exception as e:
            flash(f'Error loading admin metrics: {str(e)}', 'danger')

    return render_template('admin_dashboard.html', users=users, internships=internships, stats=stats)

@admin_bp.route('/admin/user/<string:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    if session.get('role') != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))

    if user_id == session.get('user_id'):
        flash('Cannot delete your own admin account!', 'warning')
        return redirect(url_for('admin.dashboard'))

    if supabase:
        try:
            supabase.table('users').delete().eq('id', user_id).execute()
            flash('User account deleted successfully.', 'success')
        except Exception as e:
            flash(f'Error deleting user: {str(e)}', 'danger')

    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/internship/<string:internship_id>/delete', methods=['POST'])
def delete_internship(internship_id):
    if session.get('role') != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))

    if supabase:
        try:
            supabase.table('internships').delete().eq('id', internship_id).execute()
            flash('Internship listing deleted successfully.', 'success')
        except Exception as e:
            flash(f'Error deleting internship: {str(e)}', 'danger')

    return redirect(url_for('admin.dashboard'))
