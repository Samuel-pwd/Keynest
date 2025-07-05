# run.py
import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()  # Load environment variables

app = create_app()

@app.cli.command("clear_users")
def clear_users():
    from app.models import User
    from app import db
    User.query.delete()
    db.session.commit()
    print("✅ All users deleted.")

if __name__ == '__main__':
    app.run(debug=True)
