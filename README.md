# Entitlement Calculator

A config-driven pay and leave entitlement calculator in Python and SQL, with unit tests, an audit log and reconciliation.

> **Synthetic data and illustrative rules only.** This project uses randomly generated employee data and simplified example rules. It does not use real payroll data or the rules of any actual industrial agreement.

## Why I built it
Entitlement calculations need to be accurate, auditable and easy to update when rules change. Here the rules live in a versioned config file instead of the code, and every calculation is logged with the rule version used.

## What it does
1. Generates 500 synthetic employee records, including a few deliberately bad ones
2. Validates records and rejects invalid ones (negative hours, missing rates)
3. Calculates ordinary pay, two-band overtime and leave accrual from `rules.yaml`
4. Writes results and rejected records to a SQLite audit database
5. Reconciles the SQL total against the pandas total

## Results
- 497 records valid, 3 rejected (2 negative hours, 1 missing rate)
- Reconciliation: **PASS**. Total gross pay $2,298,619.19 in both SQL and pandas
- 3 unit tests passing

See `analysis.ipynb` for the pay distribution and the rejected records.

## How to run
```
pip install -r requirements.txt
pytest
python generate_data.py
python run_pipeline.py
```
Then open `analysis.ipynb`.

## Project structure
| File | Purpose |
|------|---------|
| `rules.yaml` | Pay and leave rules, versioned |
| `calculator.py` | Calculation engine |
| `test_calculator.py` | Unit tests |
| `generate_data.py` | Synthetic data generator |
| `run_pipeline.py` | Validation, calculation, audit log and reconciliation |
| `analysis.ipynb` | Results analysis and charts |

## Limitations and next steps
- Rules are simplified and do not reflect any real agreement
- Next: PostgreSQL in place of SQLite, a rule-change impact report (old rules vs new), and a dashboard
