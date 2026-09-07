from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.supabase_client import supabase

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'student')

        if not name or not email or not password:
            flash('Please fill in all required fields.', 'danger')
            return render_template('register.html')

        if role not in ['student', 'company']:
            flash('Invalid role selected.', 'danger')
            return render_template('register.html')

        if not supabase:
            flash('Database connection unavailable. Please ensure SUPABASE environment variables are set.', 'danger')
            return render_template('register.html')

        try:
            # Check existing user
            existing = supabase.table('users').select('*').eq('email', email).execute()
            if existing.data and len(existing.data) > 0:
                flash('An account with this email address already exists.', 'warning')
                return redirect(url_for('auth.register'))

            hashed_password = generate_password_hash(password)

            # Insert new user
            insert_res = supabase.table('users').insert({
                'name': name,
                'email': email,
                'password_hash': hashed_password,
                'role': role
            }).execute()

            if insert_res.data:
                flash('Registration successful! Please log in to your account.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Could not create account. Please try again.', 'danger')
        except Exception as e:
            flash(f'Registration error: {str(e)}', 'danger')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif role == 'company':
            return redirect(url_for('company.dashboard'))
        else:
            return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please provide both email and password.', 'danger')
            return render_template('login.html')

        if not supabase:
            flash('Database connection unavailable. Please check configuration.', 'danger')
            return render_template('login.html')

        try:
            res = supabase.table('users').select('*').eq('email', email).execute()
            users = res.data if res.data else []

            if users and check_password_hash(users[0]['password_hash'], password):
                user = users[0]
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_email'] = user['email']
                session['role'] = user['role']

                flash(f'Welcome back, {user["name"]}!', 'success')

                if user['role'] == 'admin':
                    return redirect(url_for('admin.dashboard'))
                elif user['role'] == 'company':
                    return redirect(url_for('company.dashboard'))
                else:
                    return redirect(url_for('student.dashboard'))
            else:
                flash('Invalid email or password. Please try again.', 'danger')
        except Exception as e:
            flash(f'Login error: {str(e)}', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))
