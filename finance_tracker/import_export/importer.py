import csv
from finance_tracker.database import get_session
from finance_tracker.models import Expense, Budget

def import_from_csv(filename: str):
    """Import expenses and budgets from CSV file."""
    session = get_session()
    try:
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Type"] == "Expense":
                    session.add(Expense(description=row["Name"], amount=float(row["Amount"])))
                elif row["Type"] == "Budget":
                    session.add(Budget(category=row["Name"], limit=float(row["Amount"])))
        session.commit()
        print(f"✅ Data imported from {filename}")
    finally:
        session.close()


