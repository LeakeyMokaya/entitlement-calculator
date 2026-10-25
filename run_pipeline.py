import sqlite3
from datetime import datetime, timezone
import pandas as pd
from calculator import calculate_pay, load_rules

rules = load_rules()
df = pd.read_csv("data/employees.csv")

# Validate: reject negative hours or missing rates
valid = df[(df.hours_worked >= 0) & df.hourly_rate.notna()].copy()
rejected = df.drop(valid.index)
print(f"{len(valid)} valid, {len(rejected)} rejected")

results = valid.apply(
    lambda r: calculate_pay(r.hours_worked, r.hourly_rate, rules),
    axis=1, result_type="expand",
)
out = pd.concat([valid.reset_index(drop=True), results.reset_index(drop=True)], axis=1)
out["calculated_at"] = datetime.now(timezone.utc).isoformat()

con = sqlite3.connect("audit.db")
out.to_sql("calc_audit", con, if_exists="replace", index=False)
rejected.to_sql("rejected_records", con, if_exists="replace", index=False)

# Reconcile SQL total against pandas total
sql_total = con.execute("SELECT ROUND(SUM(gross_pay), 2) FROM calc_audit").fetchone()[0]
pandas_total = round(out.gross_pay.sum(), 2)
status = "PASS" if abs(sql_total - pandas_total) < 0.01 else "FAIL"
print(f"Reconciliation {status}: SQL {sql_total} vs pandas {pandas_total}")
con.close()