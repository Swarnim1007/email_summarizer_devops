from flask import Blueprint, render_template, request,redirect, url_for, session
from .models import db, Email
from .email_fetcher import fetch_and_summarize_emails

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('login.html')

@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # Perform login validation here
        # For example, check username and password against database
        # Dummy validation for demonstration purpose
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            # Fetch emails upon user login
            fetch_and_summarize_emails()
            return redirect(url_for('routes.dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')

@bp.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('routes.index'))

    # Fetch all emails from the database
    all_emails = Email.query.all()
    
    unread_emails = []
    read_emails = []
    for email in all_emails:
        if email.read:
            read_emails.append(email)
        else:
            unread_emails.append(email)
            # Mark unread emails as read
            email.read = True
            db.session.commit()

    return render_template('dashboard.html', read_email_summaries=read_emails, unread_email_summaries=unread_emails)

@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('routes.index'))
