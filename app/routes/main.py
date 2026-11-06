from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import login_required, current_user
from datetime import datetime
from app.decorator import permission_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('views/home.html', current_year=datetime.utcnow().year)
    

@main.route('/events')
def events():
    search_query = request.args.get('q', '')
    event_type = request.args.get('type', '')
    location = request.args.get('location', 'Austin, TX')
    
    return render_template(
        'views/events.html',
        current_year=datetime.utcnow().year,
        search_query=search_query,
        event_type=event_type,
        location=location
            
    )

@main.route('/event-detail')
def event_detail():
    return render_template('views/event_detail.html')

    
@main.route('/dashboard')
@login_required
def dashboard():

    return render_template('views/dashboard.html')

@main.route('/admin')
@login_required
def admin():
    "Display the admin panel"
    return "Admin Page"