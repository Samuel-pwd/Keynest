import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = str(os.environ.get('SECRET_KEY') or secrets.token_hex(32))
    
    # SQLAlchemy configuration (SQLite database stored in /instance folder)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
          'sqlite:///' + os.path.join(basedir, 'instance', 'keynest.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gmail SMTP email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # your Gmail address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # your 16-character app password
    MAIL_DEFAULT_SENDER = ('Nest', MAIL_USERNAME)    # Emails will show 'NestGuard <keynest.manager@gmail.com>'

