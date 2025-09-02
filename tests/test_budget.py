import tempfile
from finance_tracker.database import get_session, init_db, engine, Base
from finance_tracker.models import User, Category, Budget

def test_budget_create(tmp_path, monkeypatch):
    # use a temporary SQLite file for isolation
    db_file = tmp_path / "test_db.sqlite"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")
    # re-import engine/session if necessary - simpler: call init_db then use get_session()
    init_db()
    session = get_session()
    # create user and category
    u = User(name="Test", email="t@test.com")
    session.add(u); session.commit()
    c = Category(name="TestCat", type="expense")
    session.add(c); session.commit()
    b = Budget(user_id=u.id, category_id=c.id, month="2025-08", amount=100.0)
    session.add(b); session.commit()
    assert session.query(Budget).filter_by(user_id=u.id).count() == 1
    session.close()
