# HR Analytics System

Data cleaning + metrics calculation system built for Wits PGDip Programming for Data Science.

## What This Project Does

| Component | What It Does |
|-----------|---------------|
| `cleaner.py` | Removes null salaries, standardizes department names, validates performance ratings (0-5), fixes date formats, validates hire dates (2015-2025) with leap year logic |
| `metrics.py` | Calculates retention rate, turnover by department, average age, average salary by age range, and performance by training hours |
| `sql_cleaning_queries.sql` | Same cleaning logic written in SQL – adapted for equipment maintenance data (MTBF, uptime, failure rates) |

## Skills Demonstrated

- Python data cleaning (null handling, validation, date logic)
- Business metric calculation from raw data
- SQL equivalents for ERP/maintenance databases
- Edge case handling (leap years, empty datasets, out-of-range values)
- Testing with Pytest

## Industrial Transferability

This HR analytics logic applies directly to **equipment maintenance data**:

| HR Concept | Maintenance Equivalent |
|------------|----------------------|
| Retention rate | Equipment uptime percentage |
| Turnover rate | Failure rate by component |
| Average salary by age | Average MTBF by equipment class |
| Performance by training | Performance by maintenance hours |

## How to Run

```bash
# Clone the repository
git clone https://github.com/RebeccaDataSci/hr-analytics-system.git

# Generate fake data
cd hr-analytics-system/data
python generate_fake_hr_data.py

# Run cleaning and metrics
cd ../src
python cleaner.py
python metrics.py

# Run tests
pytest tests/
