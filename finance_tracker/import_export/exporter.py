import csv
from finance_tracker.database import get_session
from finance_tracker.models import Expense, Budget

def export_to_csv(filename: str = "finance_export.csv"):
    """Export all data to a CSV file."""
    session = get_session()
    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Name", "Amount", "Date/Limit"])

            for expense in session.query(Expense).all():
                writer.writerow(["Expense", expense.description, expense.amount, expense.date])

            for budget in session.query(Budget).all():
                writer.writerow(["Budget", budget.category, budget.limit, "N/A"])
        print(f"✅ Data exported to {filename}")
    finally:
        session.close()
