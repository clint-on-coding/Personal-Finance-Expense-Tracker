💰 Personal Finance Expense Tracker

A simple yet powerful command-line personal finance tracker built with Python, SQLAlchemy, and SQLite.
It allows users to record budgets and expenses while automatically sending email notifications with budget summaries and expense updates.

🚀 Features

📊 Record Budgets

Add a new budget limit for your finances.

Receive an email confirmation when a budget is added.

🧾 Track Expenses

Log expenses with a description and amount.

Automatically get an email update showing:

Your current budget balance.

The latest expense recorded.

📩 Email Notifications

Budgets and expenses are shared via email.

Uses Gmail’s App Passwords for secure sending.

🗄️ SQLite Database

All budgets and expenses are stored persistently.

⚙️ Installation

Clone the Repository

git clone https://github.com/your-username/Personal-Finance-Expense-Tracker.git
cd Personal-Finance-Expense-Tracker


Create and Activate a Virtual Environment

python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


Install Dependencies

pip install -r requirements.txt


Set Up Environment Variables
Create a .env file in the project root:

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password


⚠️ Use a Gmail App Password, not your normal Gmail password.
You must enable 2FA in Gmail, then create an App Password.

Initialize the Database

python main.py init-db

📌 Usage
Add a Budget
python main.py add-budget 500


✅ Adds a budget of 500 and sends an email.

Add an Expense
python main.py add-expense "Groceries" 120


✅ Logs an expense and sends an email with:

Remaining budget

Expense details

Send Budget Summary Manually
python main.py send-budget


✅ Sends the current budget balance via email.

🛠️ Tech Stack

Python 3.8+

SQLAlchemy – ORM for database management

SQLite – Lightweight local database

Click – For building the command-line interface

smtplib + dotenv – Secure email notifications

📧 Email Notifications Example

Subject: 💰 New Expense Recorded

Expense: Groceries - 120.0
Remaining Budget: 380.0


Subject: 💰 New Budget Recorded

A new budget of 500.0 has been set!

🏆 Future Improvements

Add categories for budgets and expenses.

Generate monthly reports.

Add visual dashboards (charts/graphs).

Export to CSV/Excel.

👨‍💻 Author

Clinton Mwangi

📧 Email: clintonmwangi10636@gmail.com

💼 LinkedIn

💻 GitHub

Would you like me to make it short and professional for school submission, or long and detailed (with screenshots, email previews, etc.) for GitHub portfolio?

You said:
short and professional for school submission
ChatGPT said:

Got it ✅ — here’s a short, professional README you can submit for school:

Personal Finance Expense Tracker

A command-line application for managing personal finances. Built with Python, SQLAlchemy, and SQLite, it allows users to add budgets and record expenses while sending automatic email notifications for updates.

Features

Add and track budgets.

Record expenses with descriptions and amounts.

Automatic email notifications for new budgets and expenses.

Persistent storage using SQLite.

Installation

Clone the repository:

git clone https://github.com/your-username/Personal-Finance-Expense-Tracker.git
cd Personal-Finance-Expense-Tracker


Install dependencies:

pip install -r requirements.txt


Create a .env file with your Gmail credentials:

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password


Initialize the database:

python main.py init-db

Usage

Add a budget:

python main.py add-budget 500


Add an expense:

python main.py add-expense "Groceries" 100


Send budget summary:

python main.py send-budget

Author

Clinton Mwangi
