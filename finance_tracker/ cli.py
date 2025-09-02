from datetime import date, datetime
from finance_tracker.database import get_session
from finance_tracker.models import User, Category, Budget, Transaction
from finance_tracker.email_utils import send_email, send_budget_email, send_expense_email
from finance_tracker.import_export import export_data_to_csv, import_data_from_csv
from finance_tracker.utils import pretty_table
from sqlalchemy import func

def main_menu(session):
    while True:
        print("\n=== Finance Tracker ===")
        print("1) Add user")
        print("2) Add category")
        print("3) Set budget")
        print("4) Add transaction (expense/income)")
        print("5) List transactions")
        print("6) Export data (CSV)")
        print("7) Import data (CSV)")
        print("8) Report")
        print("0) Exit")

        choice = input("Choose: ").strip()
        if choice == "1":
            add_user(session)
        elif choice == "2":
            add_category(session)
        elif choice == "3":
            set_budget(session)
        elif choice == "4":
            add_transaction(session)
        elif choice == "5":
            list_transactions(session)
        elif choice == "6":
            fname = input("Filename (default finance_data.csv): ").strip() or "finance_data.csv"
            export_data_to_csv(session, fname)
        elif choice == "7":
            fname = input("Filename to import (default finance_data.csv): ").strip() or "finance_data.csv"
            import_data_from_csv(session, fname)
        elif choice == "8":
            report(session)
        elif choice == "0":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice")

def add_user(session):
    email = input("Email: ").strip()
    name = input("Name (optional): ").strip() or None
    if session.query(User).filter_by(email=email).first():
        print("User exists.")
        return
    u = User(email=email, name=name)
    session.add(u); session.commit()
    print(f"Created user {email}")

def add_category(session):
    name = input("Category name: ").strip()
    typ = input("Type (income/expense): ").strip().lower()
    if typ not in ("income","expense"):
        print("Invalid type")
        return
    if session.query(Category).filter_by(name=name).first():
        print("Category exists.")
        return
    c = Category(name=name, type=typ)
    session.add(c); session.commit()
    print(f"Created category {name} ({typ})")

def choose_user(session):
    users = session.query(User).order_by(User.id).all()
    if not users:
        print("No users. Add a user first.")
        return None
    list_rows = [(u.id, u.email, u.name or "-") for u in users]
    pretty_table(["ID","Email","Name"], list_rows)
    uid = int(input("Select user id: "))
    return session.get(User, uid)

def choose_category(session, typ=None):
    q = session.query(Category)
    if typ:
        q = q.filter_by(type=typ)
    cats = q.order_by(Category.name).all()
    if not cats:
        print("No categories.")
        return None
    pretty_table(["ID","Name","Type"], [(c.id,c.name,c.type) for c in cats])
    cid = int(input("Select category id: "))
    return session.get(Category, cid)

def set_budget(session):
    user = choose_user(session)
    if not user:
        return
    cat = choose_category(session, typ="expense")
    if not cat:
        return
    month = input("Month (YYYY-MM) default current: ").strip() or f"{date.today().year}-{date.today().month:02d}"
    amount = float(input("Budget amount: ").strip())
    b = session.query(Budget).filter_by(user_id=user.id, category_id=cat.id, month=month).one_or_none()
    if b:
        b.amount = amount
        print("Updated budget.")
    else:
        b = Budget(user_id=user.id, category_id=cat.id, month=month, amount=amount)
        session.add(b)
        print("Created budget.")
    session.commit()
    # send email summarizing the budget
    send_budget_email(session, b)

def add_transaction(session):
    user = choose_user(session)
    if not user:
        return
    typ = input("Type (income/expense): ").strip().lower()
    if typ not in ("income","expense"):
        print("Invalid type")
        return
    cat = choose_category(session, typ=typ)
    if not cat:
        return
    amount = float(input("Amount: ").strip())
    desc = input("Description (optional): ").strip() or None
    date_str = input("Date (YYYY-MM-DD) default today: ").strip() or date.today().isoformat()
    dt = datetime.fromisoformat(date_str).date()
    txn = Transaction(user_id=user.id, category_id=cat.id, amount=amount, date=dt, description=desc, type=typ)
    session.add(txn); session.commit()
    print("Transaction recorded.")
    # If expense, email budget summary + expense
    if typ == "expense":
        send_expense_email(session, txn)

def list_transactions(session):
    user = choose_user(session)
    if not user:
        return
    txns = session.query(Transaction).filter_by(user_id=user.id).order_by(Transaction.date.desc()).all()
    if not txns:
        print("No transactions.")
        return
    rows = [(t.id, t.date, t.type, t.category.name, f"{t.amount:.2f}", t.description or "") for t in txns]
    pretty_table(["ID","Date","Type","Category","Amount","Description"], rows)

def report(session):
    users = session.query(User).all()
    for u in users:
        print(f"\nUser: {u.email} ({u.name or '-'})")
        # budgets
        budgets = session.query(Budget).filter_by(user_id=u.id).all()
        print(" Budgets:")
        for b in budgets:
            print(f"  - {b.month} {b.category.name if b.category else b.category_id}: {b.amount:.2f}")
        # expenses summary
        from sqlalchemy import func
        expenses = session.query(Transaction.category_id, func.sum(Transaction.amount)).filter_by(user_id=u.id, type="expense").group_by(Transaction.category_id).all()
        print(" Expenses (by category):")
        for cid, total in expenses:
            cat = session.query(Category).get(cid)
            print(f"  - {cat.name if cat else cid}: {total:.2f}")
