import smtplib
from email.mime.text import MIMEText
from .utils import format_currency
from .models import Budget, Expense

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"   # replace with your Gmail
SENDER_PASSWORD = "your_app_password"   # replace with your Gmail App Password

def send_email(subject: str, body: str, recipient_email: str) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())

def send_budget_email(budget: Budget, recipient_email: str) -> None:
    subject = "Your Current Budget"
    body = f"Your budget is {format_currency(budget.amount)}."
    send_email(subject, body, recipient_email)

def send_expense_email(expense: Expense, recipient_email: str) -> None:
    subject = "New Expense Added"
    body = f"You spent {format_currency(expense.amount)} on {expense.description}."
    send_email(subject, body, recipient_email)


