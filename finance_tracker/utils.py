import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure these (use environment variables in production!)
EMAIL_ADDRESS = "clintonmwangi10636@gmail.com"
EMAIL_PASSWORD = "ulvjrhllefrmxzyv"
TO_EMAIL = "clintonmwangi10636@gmail.com"

def send_email(subject, body):
    """Send an email with HTML formatting"""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    # Attach HTML body
    html_part = MIMEText(body, "html")
    msg.attach(html_part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        print(f"✅ Email sent: {subject}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
