from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.supabase_client import supabase

company_bp = Blueprint('company', __name__)

@company_bp.route('/company/dashboard')
def dashboard():
    if session.get('role') != 'company':
        flash('Unauthorized access. Company portal required.', 'danger')
        return redirect(url_for('auth.login'))

    company_id = session.get('user_id')
    internships = []
    applications = []

    if supabase:
        try:
            # Fetch company posted internships
            intern_res = supabase.table('internships').select('*').eq('company_id', company_id).order('created_at', desc=True).execute()
            if intern_res.data:
                internships = intern_res.data
                
                # Fetch all applications for company's internships
                internship_ids = [item['id'] for item in internships]
                if internship_ids:
                    app_res = supabase.table('applications').select('*, internships(title), users:student_id(name, email)').in_('internship_id', internship_ids).order('applied_at', desc=True).execute()
                    if app_res.data:
                        applications = app_res.data
        except Exception as e:
            flash(f'Error loading company dashboard: {str(e)}', 'danger')

    return render_template('company_dashboard.html', internships=internships, applications=applications)

@company_bp.route('/company/add-internship', methods=['GET', 'POST'])
def add_internship():
    if session.get('role') != 'company':
        flash('Unauthorized access. Company portal required.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        requirements = request.form.get('requirements', '').strip()
        location = request.form.get('location', 'Remote').strip()
        stipend = request.form.get('stipend', 'Unpaid').strip()
        company_id = session.get('user_id')

        if not title or not description:
            flash('Title and Description are required.', 'danger')
            return render_template('add_internship.html')

        if not supabase:
            flash('Database connection unavailable.', 'danger')
            return render_template('add_internship.html')

        try:
            supabase.table('internships').insert({
                'company_id': company_id,
                'title': title,
                'description': description,
                'requirements': requirements,
                'location': location,
                'stipend': stipend
            }).execute()

            flash('Internship opportunity posted successfully!', 'success')
            return redirect(url_for('company.dashboard'))
        except Exception as e:
            flash(f'Error posting internship: {str(e)}', 'danger')

    return render_template('add_internship.html')

@company_bp.route('/company/application/<string:application_id>/status', methods=['POST'])
def update_application_status(application_id):
    if session.get('role') != 'company':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))

    new_status = request.form.get('status')
    if new_status not in ['Accepted', 'Rejected', 'Pending']:
        flash('Invalid status provided.', 'danger')
        return redirect(url_for('company.dashboard'))

    if supabase:
        try:
            supabase.table('applications').update({'status': new_status}).eq('id', application_id).execute()
            flash(f'Application status updated to {new_status}.', 'success')
        except Exception as e:
            flash(f'Error updating status: {str(e)}', 'danger')

    return redirect(url_for('company.dashboard'))
