import pytest
from calculator import calculate_pay, load_rules

RULES = load_rules()

def test_no_overtime():
    assert calculate_pay(76, 40, RULES)["gross_pay"] == 3040.00

def test_overtime_two_bands():
    assert calculate_pay(90, 40, RULES)["gross_pay"] == 4000.00

def test_leave_accrual():
    assert calculate_pay(76, 40, RULES)["leave_accrued_hours"] == pytest.approx(5.846, abs=0.001)
