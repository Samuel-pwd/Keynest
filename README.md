# 🔐 KeyNest – Password Manager

KeyNest is a secure, beginner-friendly password manager built with Flask. It offers core authentication features like user registration, email verification, login, and password reset — all styled with a modern frosted glass UI (glassmorphism).

---

## 🚀 Features

- User registration with email verification  
- Login using username or email  
- Password reset via secure token sent to email  
- Passwords stored using bcrypt hashing  
- Flash messaging and access control  
- Clean, responsive UI (glassmorphism theme)  
- Environment-secured credentials using `.env` and `.gitignore`  

---

## 🖼️ Screenshots

### 🔑 Login Page
![Login Screenshot](screenshots/login.png)

### 🧾 Registration Page
![Registration Screenshot](screenshots/registration.png)

### 🔄 Reset Password Page
![Reset Password Screenshot](screenshots/reset-password.png)

---

## 📁 Project Structure

```bash
keynest/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   ├── routes.py
│   ├── forms.py
│   ├── models.py
│   └── ...
├── migrations/
├── screenshots/
├── requirements.txt
├── run.py
├── config.py
├── .env
└── .gitignore
```

---

## 🛠️ Setup Instructions

```bash
# 1. Clone the repository
git clone git@github.com:Samuel-pwd/Keynest.git
cd Keynest

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your environment (.env)
SECRET_KEY=your_secret_key
MAIL_USERNAME=your_email
MAIL_PASSWORD=your_email_password_or_brevo_key

# 5. Run the Flask app
python run.py
```

---

## ✍️ Author

**Otieno Samuel**  
GitHub: [@Samuel-pwd](https://github.com/Samuel-pwd)

---

## 🧭 Notes

- This repository is a **live journey** documenting growth from scratch.
- Screenshots capture real milestones and UI improvements.
- Secrets like API keys are excluded from version control for security.
- Future plans include encryption, user vaults, and database upgrades.

---

## 📜 License

This project is licensed under the **MIT License**.
