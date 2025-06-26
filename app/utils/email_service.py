import requests
from flask import current_app

def send_verification_email(recipient_email, verification_link):
    brevo_url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": current_app.config.get('BREVO_SENDER_NAME'),
            "email": current_app.config.get('BREVO_SENDER_EMAIL')
        },
        "to": [{"email": recipient_email}],
        "subject": "Verify Your NestGuard Account", # Updated subject for your brand
        "htmlContent": f"""
            <p>Welcome to NestGuard! Please click the link below to verify your email address:</p>
            <p><a href="{verification_link}" style="display: inline-block; padding: 10px 20px; background-color: #0095f6; color: white; text-decoration: none; border-radius: 5px;">Verify Your Account</a></p>
            <p>If you did not register for NestGuard, please ignore this email.</p>
            <p>Link: {verification_link}</p>
        """
    }

    headers = {
        "accept": "application/json",
        "api-key": current_app.config.get('BREVO_API_KEY'),
        "content-type": "application/json"
    }

    try:
        response = requests.post(brevo_url, json=payload, headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        if response.status_code == 201:
            current_app.logger.info(f"Verification email sent to {recipient_email}")
            return True
        else:
            current_app.logger.error(f"Brevo email failed: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error sending email via Brevo: {e}")
        return False