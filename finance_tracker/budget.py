# finance_tracker/budget.py
from .models import Budget

def record_budget(category, limit, start_date, end_date):
    """Create and return a new budget object"""
    budget = Budget(
        id=None,  # if using a DB, this will be auto-set
        category=category,
        limit=limit,
        start_date=start_date,
        end_date=end_date
    )
    return budget
