from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from app.models import User
from app import db, bcrypt, mail
from flask_mail import Message
from sqlalchemy import or_

main = Blueprint('main', __name__)

# Home
@main.route('/')
@main.route('/dashboard')
def home():
    if current_user.is_authenticated:
        return render_template('dashboard.html', title='Dashboard', user=current_user)
    return redirect(url_for('main.login'))

# Registration
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw, is_verified=False)
        db.session.add(user)
        db.session.commit()

        token = user.get_verification_token()
        verification_link = url_for('main.verify_email', token=token, _external=True)

        try:
            msg = Message('Verify Your Nestguard Account', recipients=[user.email])
            msg.html = f"""
                <p>Welcome to KeyNest! Please click the link below to verify your email address:</p>
                <p><a href="{verification_link}" style="display: inline-block; padding: 10px 20px; background-color: #0095f6; color: white; text-decoration: none; border-radius: 5px;">Verify Your Account</a></p>
                <p>If you did not register for KeyNest, please ignore this email.</p>
                <p>Link: {verification_link}</p>
            """
            mail.send(msg)
            flash('Account created! A verification email has been sent. Please check your inbox.', 'info')
        except Exception as e:
            current_app.logger.error(f"Failed to send verification email to {user.email}: {e}")
            flash('Account created, but failed to send verification email. Please try again later.', 'warning')

        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

# Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.identifier.data
        user = User.query.filter(or_(User.email == identifier, User.username == identifier)).first()

        print("DEBUG LOGIN:")
        print("Identifier:", identifier)
        print("User exists:", bool(user))
        if user:
            print("User password hash:", user.password)
            print("Is verified:", user.is_verified)
            print("Password correct:", bcrypt.check_password_hash(user.password, form.password.data))

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if not user.is_verified:
                flash('Your account is not verified. Please check your email.', 'warning')
                return render_template('login.html', form=form)
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully!', 'success')
            return redirect(request.args.get('next') or url_for('main.home'))

        flash('Login failed. Check your username/email and password.', 'danger')

    return render_template('login.html', form=form)

# Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

# Forgot Password
@main.route('/forget-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            reset_link = url_for('main.reset_token', token=token, _external=True)

            try:
                msg = Message('Password Reset Request - KeyNest', recipients=[user.email])
                msg.html = f'''
                    <p>To reset your password, click the link below:</p>
                    <p><a href="{reset_link}">Reset Password</a></p>
                    <p>This link expires in 1 hour.</p>
                '''
                mail.send(msg)
                flash('A password reset link has been sent to your email.', 'info')
            except Exception as e:
                flash('Failed to send email. Try again later.', 'danger')
        else:
            flash('No account found with that email.', 'danger')

        return redirect(url_for('main.forgot_password'))

    return render_template('forgot_password.html', form=form)

# Reset Password
@main.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.forgot_password'))
    
    user = User.verify_reset_token(token)
    if user is None:
        return render_template('errors/expired_token.html'), 403

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('reset_password.html', form=form)

# Email Verification
@main.route('/verify/<token>')
def verify_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_verification_token(token)
    if user is None:
        flash('That is an invalid or expired verification link.', 'danger')
        return redirect(url_for('main.register'))

    if user.is_verified:
        if not current_user.is_authenticated:
            login_user(user)
        flash('Your account is already verified. You are now logged in.', 'info')
        return redirect(url_for('main.home'))

    user.is_verified = True
    db.session.commit()
    flash('Your email has been successfully verified! Please log in to continue.', 'success')
    return redirect(url_for('main.login'))


#Dashboard
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# Debug route to list all users (DEV ONLY)
@main.route('/debug-users')
def debug_users():
    users = User.query.all()
    output = [f"{u.username} | {u.email} | Verified: {u.is_verified}" for u in users]
    return "<br>".join(output)
