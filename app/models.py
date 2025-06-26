# app/models.py

from app import db
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app  # Needed for current_app.config['SECRET_KEY']


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    keys = db.relationship('Key', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', Verified: {self.is_verified})"

    # Email Verification Token
    def get_verification_token(self, expires_sec=3600):
        """
        Generate a secure, time-limited token for email verification (default 1 hour).
        """
        secret_key_bytes = current_app.config['SECRET_KEY'].encode('utf-8')
        s = Serializer(secret_key_bytes, salt='email-confirm')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_verification_token(token, max_age=3600):
        """
        Verify the email confirmation token.
        """
        secret_key_bytes = current_app.config['SECRET_KEY'].encode('utf-8')
        s = Serializer(secret_key_bytes, salt='email-confirm')
        try:
            user_id = s.loads(token, max_age=max_age)['user_id']
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(user_id)

    # Password Reset Token
    def get_reset_token(self, expires_sec=1800):
        """
        Generate a secure, time-limited token for password reset (default 30 minutes).
        """
        secret_key_bytes = current_app.config['SECRET_KEY'].encode('utf-8')
        s = Serializer(secret_key_bytes, salt='password-reset')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        """
        Verify the password reset token.
        """
        secret_key_bytes = current_app.config['SECRET_KEY'].encode('utf-8')
        s = Serializer(secret_key_bytes, salt='password-reset')
        try:
            user_id = s.loads(token, max_age=max_age)['user_id']
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(user_id)


class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(500), nullable=False)  # The actual key/credential
    description = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Key('{self.title}', '{self.date_added}')"
