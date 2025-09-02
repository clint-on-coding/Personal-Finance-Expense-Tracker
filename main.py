import click
from sqlalchemy.sql import func
from finance_tracker.models import Budget, Expense
from finance_tracker.database import SessionLocal
from finance_tracker.utils import send_email

session = SessionLocal()

@click.group()
def cli():
    pass

# -----------------------------
# Add Budget
# -----------------------------
@cli.command()
@click.argument("amount", type=float)
def add_budget(amount):
    """Add a new budget"""
    budget = Budget(limit=amount, category="General")
    session.add(budget)
    session.commit()

    # Send email notification
    subject = "💰 New Budget Recorded"
    body = f"""
    <h2>Budget Recorded</h2>
    <p><b>Category:</b> {budget.category}</p>
    <p><b>Limit:</b> ${budget.limit:.2f}</p>
    """
    send_email(subject, body)
    click.echo(f"Budget of {amount} added successfully!")


# -----------------------------
# Add Expense
# -----------------------------
@cli.command()
@click.argument("description")
@click.argument("amount", type=float)
def add_expense(description, amount):
    """Add a new expense"""
    expense = Expense(description=description, amount=amount)
    session.add(expense)
    session.commit()

    # Get latest budget
    budget = session.query(Budget).order_by(Budget.id.desc()).first()
    total_expenses = session.query(Expense).with_entities(
        func.sum(Expense.amount)
    ).scalar() or 0
    remaining_balance = budget.limit - total_expenses if budget else 0

    # Send email notification
    subject = "💸 New Expense Recorded"
    body = f"""
    <h2>Expense Recorded</h2>
    <p><b>Description:</b> {expense.description}</p>
    <p><b>Amount:</b> ${expense.amount:.2f}</p>
    <hr>
    <h3>💰 Current Budget Status</h3>
    <p><b>Budget Limit:</b> ${budget.limit:.2f}</p>
    <p><b>Total Spent:</b> ${total_expenses:.2f}</p>
    <p><b>Remaining Balance:</b> ${remaining_balance:.2f}</p>
    """
    send_email(subject, body)
    click.echo(f"Expense '{description}' of {amount} added successfully!")

if __name__ == "__main__":
    cli()

