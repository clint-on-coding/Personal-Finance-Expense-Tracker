# finance_tracker/reports.py
from typing import List, Optional
from .models import Expense, Budget
from .utils import format_currency, get_current_budget, total_expenses, remaining_budget

def generate_report(budgets: List[Budget], expenses: List[Expense]) -> str:
    budget = get_current_budget(budgets)
    if not budget:
        return "No budget found."

    total = total_expenses(expenses)
    remaining = remaining_budget(budget, expenses)

    report = [
        f"Budget Report",
        f"==============",
        f"Total Budget: {format_currency(budget.amount)}",
        f"Total Expenses: {format_currency(total)}",
        f"Remaining Budget: {format_currency(remaining)}",
        "",
        "Expenses:",
    ]

    for exp in expenses:
        report.append(f"- {exp.description}: {format_currency(exp.amount)}")

    return "\n".join(report)
