from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from extensions import db
from models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
        
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        username = request.form.get('username').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not email or not username or not password:
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')
            
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')
            
        # Check if email or username already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email address already registered.', 'danger')
            return render_template('auth/register.html')
            
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken.', 'danger')
            return render_template('auth/register.html')
            
        # Create new user
        new_user = User(email=email, username=username)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            # Seed mock focus data to showcase graphs beautifully
            from seeder import seed_user_data
            seed_user_data(new_user)
            
            flash('Registration successful! Your dashboard has been seeded with mock data so you can see analytics immediately.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
        
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('auth/login.html')
            
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'danger')
            return render_template('auth/login.html')
            
        login_user(user, remember=remember)
        flash(f'Welcome back, {user.username}!', 'success')
        
        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard.home'))
        
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out successfully.', 'success')
    return redirect(url_for('dashboard.landing'))
