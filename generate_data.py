import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 500
df = pd.DataFrame({
    "employee_id": [f"E{i:04d}" for i in range(1, n + 1)],
    "hourly_rate": rng.uniform(32, 85, n).round(2),
    "hours_worked": rng.normal(78, 6, n).clip(40, 110).round(1),
})

# Inject a few bad records to test data validation
df.loc[[10, 77], "hours_worked"] = -5
df.loc[150, "hourly_rate"] = np.nan

os.makedirs("data", exist_ok=True)
df.to_csv("data/employees.csv", index=False)
print("C:/Users/LEAKEY_ITGUY/entitlement-calculator/employees.csv")