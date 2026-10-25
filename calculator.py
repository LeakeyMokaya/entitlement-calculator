
import yaml

def load_rules(path="rules.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def calculate_pay(hours_worked, hourly_rate, rules):
    cap = rules["ordinary_hours_per_fortnight"]
    ordinary = min(hours_worked, cap)
    overtime = max(hours_worked - cap, 0)
    band1 = min(overtime, rules["overtime"]["band1_hours"])
    band2 = overtime - band1
    pay = (ordinary * hourly_rate
           + band1 * hourly_rate * rules["overtime"]["band1_multiplier"]
           + band2 * hourly_rate * rules["overtime"]["band2_multiplier"])
    return {
        "ordinary_hours": ordinary,
        "overtime_hours": overtime,
        "gross_pay": round(pay, 2),
        "leave_accrued_hours": round(ordinary * rules["leave_accrual_rate"], 4),
        "rules_version": rules["version"],
    }