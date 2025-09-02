import smtplib
import os
from unittest import mock
from finance_tracker.email_utils import send_email

def test_send_email_success(monkeypatch):
    # Create dummy SMTP class to capture send_message
    class DummySMTP:
        def __init__(self, host, port):
            self.host = host; self.port = port
            self.sent = []
            self.started = False
            self.logged = False

        def starttls(self):
            self.started = True

        def login(self, user, password):
            if password != "correct_pass":
                raise smtplib.SMTPAuthenticationError(535, b"Auth failed")
            self.logged = True

        def send_message(self, msg):
            self.sent.append(msg)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    dummy = DummySMTP("smtp", 587)

    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USER", "user")
    monkeypatch.setenv("SMTP_PASS", "correct_pass")
    monkeypatch.setenv("FROM_EMAIL", "from@example.com")
    monkeypatch.setenv("DEFAULT_RECIPIENT", "to@example.com")

    monkeypatch.setattr(smtplib, "SMTP", lambda host, port: dummy)

    result = send_email("Hello", "This is a test", to_email=None)
    assert result is True
    assert len(dummy.sent) == 1
    assert dummy.sent[0]["Subject"] == "Hello"
