from finance_tracker.database import get_session, init_db
from finance_tracker.models import User, Category, Transaction

def test_add_transaction(monkeypatch):
    # initialize db
    init_db()
    session = get_session()
    # create user & category
    u = User(name="T", email="t2@test.com")
    session.add(u); session.commit()
    c = Category(name="C2", type="expense")
    session.add(c); session.commit()
    tx = Transaction(user_id=u.id, category_id=c.id, type="expense", amount=10.0)
    session.add(tx); session.commit()
    assert session.query(Transaction).filter_by(user_id=u.id).count() == 1
    session.close()
