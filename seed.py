from finance_tracker.database import init_db, get_session
from finance_tracker.models import User, Category, Transaction, Budget
from datetime import date

def seed():
    init_db()
    session = get_session()

    # Create users
    if not session.query(User).filter_by(email="alice@example.com").first():
        session.add(User(name="Alice", email="alice@example.com"))
    if not session.query(User).filter_by(email="bob@example.com").first():
        session.add(User(name="Bob", email="bob@example.com"))
    session.commit()

    # Create categories if missing
    categories = [
        ("Salary","income"),
        ("Freelancing","income"),
        ("Rent","expense"),
        ("Groceries","expense"),
        ("Transport","expense"),
        ("Entertainment","expense"),
    ]
    for name, typ in categories:
        if not session.query(Category).filter_by(name=name).first():
            session.add(Category(name=name, type=typ))
    session.commit()

    # create example transactions & budgets if none exist
    alice = session.query(User).filter_by(email="alice@example.com").one()
    cats = {c.name: c for c in session.query(Category).all()}

    if session.query(Transaction).count() == 0:
        txns = [
            Transaction(user_id=alice.id, category_id=cats["Salary"].id, type="income", amount=1200.0, date=date(2025,8,1), description="August salary"),
            Transaction(user_id=alice.id, category_id=cats["Rent"].id, type="expense", amount=400.0, date=date(2025,8,2), description="Rent"),
            Transaction(user_id=alice.id, category_id=cats["Groceries"].id, type="expense", amount=120.0, date=date(2025,8,6), description="Groceries"),
        ]
        session.add_all(txns)
        session.commit()

    if not session.query(Budget).filter_by(user_id=alice.id, category_id=cats["Groceries"].id, month="2025-08").first():
        session.add(Budget(user_id=alice.id, category_id=cats["Groceries"].id, month="2025-08", amount=150.0))
        session.commit()

    session.close()
    print("Seed complete ✅")

if __name__ == "__main__":
    seed()
