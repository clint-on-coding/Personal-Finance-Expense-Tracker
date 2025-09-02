# Personal-Finance-Expense-Tracker
A command-line finance tracker to manage budgets and expenses with email notifications, CSV import/export, and simple reports.

## Setup

1. Copy `.env.example` to `.env` and fill SMTP & DB values:
   cp .env.example .env

2. Install dependencies (recommended: Pipenv) and enter shell:
pipenv install
pipenv shell

3. Initialize DB and seed demo data:
python seed.py

4. Run the app:
python main.py


Basic workflow (menu):
Add users

Record budgets (sends email)

Record expenses (sends email with budget status)

Export / Import data (CSV)

View simple report

Tests
Run tests (SMTP is mocked for safety):
pytest


Notes
Configure .env with real SMTP credentials to enable email sending.

Tests mock smtplib.SMTP, so running tests will not send real emails.

Extend with Flask/React later for a marketable web app.


---

## `main.py`
```python
from finance_tracker.cli import main_menu
from finance_tracker.database import init_db, get_session

def prepare():
    # Create DB tables (if not present)
    init_db()

if __name__ == "__main__":
    prepare()
    session = get_session()
    try:
        main_menu(session)
    finally:
        session.close()