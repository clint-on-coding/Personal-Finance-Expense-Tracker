import smtplib
from email.mime.text import MIMEText
from finance_tracker.database import get_session
from finance_tracker.models import Budget

SENDER_EMAIL = "clintonmwangi10636@gmail.com"
SENDER_PASSWORD = "ulvjrhllefrmxzyv"
RECEIVER_EMAIL = "clintonmwangi10636@gmail.com"

def send_email_notification():
    """Send a budget summary by email."""
    session = get_session()
    budgets = session.query(Budget).all()
    session.close()

    message = "📊 Budget Summary:\n\n"
    for b in budgets:
        message += f"{b.category}: Limit = {b.limit}\n"

    msg = MIMEText(message)
    msg["Subject"] = "Your Budget Summary"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

    print("✅ Email sent successfully!")
