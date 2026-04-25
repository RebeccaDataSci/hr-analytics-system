
"""
Fake HR Data Generator
Creates realistic-looking messy HR data with intentional issues:
- Null salaries (NaN)
- Inconsistent department names (mixed case, spaces)
- Invalid performance ratings (<0 or >5)
- Various date formats
- Invalid dates (future, pre-2015, Feb 29 on non-leap years)
"""

import csv
import random
from datetime import datetime, timedelta


def random_date(start_year, end_year, include_invalid=False):
    """Generate a random date between start_year and end_year"""
    if include_invalid:
        # Occasionally generate an invalid date
        invalid_type = random.choice(['future', 'past', 'impossible'])

        if invalid_type == 'future':
            # Date in 2026 or later
            year = random.randint(2026, 2030)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
        elif invalid_type == 'past':
            # Date before 2015
            year = random.randint(2000, 2014)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
        else:
            # Impossible date (Feb 30, etc.)
            month = 2
            day = 30
            year = random.randint(2015, 2025)

        try:
            return f"{year}-{month:02d}-{day:02d}"
        except:
            return "2020-13-40"  # Completely invalid
    else:
        # Valid date between 2015 and 2025
        start = datetime(start_year, 1, 1)
        end = datetime(end_year, 12, 31)
        random_date = start + timedelta(
            days=random.randint(0, (end - start).days)
        )
        # Mixed formats for realism
        format_choice = random.choice(['iso', 'dmy', 'mdy'])
        if format_choice == 'iso':
            return random_date.strftime("%Y-%m-%d")
        elif format_choice == 'dmy':
            return random_date.strftime("%d/%m/%Y")
        else:
            return random_date.strftime("%m/%d/%Y")


def generate_employee_record(emp_id, include_issues=True):
    """Generate a single employee record with optional intentional issues"""

    # Departments with inconsistent casing and spaces
    departments_raw = [
        "Engineering", "engineering", "  SALES  ", "Sales", "HR",
        "hr", "Marketing", "marketing", "Product", "product"
    ]

    # Clean version for reference (what we want after cleaning)
    departments_clean = [
        "engineering", "sales", "hr", "marketing", "product"
    ]

    if include_issues and random.random() < 0.15:  # 15% chance of weird department
        dept = random.choice(departments_raw)
    else:
        dept = random.choice(departments_clean)

    # Gender
    gender = random.choice(["Male", "Female", "Other"])

    # Age (reasonable range 20-65)
    age = random.randint(20, 65)

    # Salary - with occasional NaN
    if include_issues and random.random() < 0.1:  # 10% null salary
        salary = float('nan')
    else:
        salary = round(random.uniform(30000, 120000), 2)

    # Training hours (0-100)
    training_hours = random.randint(0, 100)

    # Performance rating - with occasional invalid
    if include_issues and random.random() < 0.08:  # 8% invalid rating
        rating = random.choice([-1, 6, 10, -5])
    else:
        rating = random.randint(0, 5)

    # Years of experience
    experience = random.randint(0, 40)

    # Employment status
    status = random.choice(
        ["Active", "Resigned", "Active", "Active"])  # 75% active

    # Hire date - with occasional invalid
    include_invalid_date = include_issues and random.random() < 0.12
    hire_date = random_date(2015, 2025, include_invalid=include_invalid_date)

    return [
        emp_id,           # Employee ID
        dept,             # Department
        gender,           # Gender
        age,              # Age
        salary,           # Salary
        training_hours,   # Training Hours
        rating,           # Performance Rating
        experience,       # Years of Experience
        status,           # Employment Status
        hire_date         # Hire Date
    ]


def generate_dataset(num_records=200, output_file='uncleaned_dataset.csv'):
    """Generate a full dataset with intentional data quality issues"""

    # Define column headers
    headers = [
        'EmpID', 'Department', 'Gender', 'Age', 'Salary',
        'Training_Hours', 'Performance_Rating', 'Years_Experience',
        'Employment_Status', 'Hire_Date'
    ]

    # Generate records
    data = []
    for emp_id in range(1, num_records + 1):
        # First 150 records have intentional issues, last 50 are clean
        include_issues = emp_id <= 150
        record = generate_employee_record(
            emp_id, include_issues=include_issues)
        data.append(record)

    # Write to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Generated {num_records} records in '{output_file}'")
    print(f"  - First 150 records include intentional data quality issues")
    print(f"  - Last 50 records are clean (for testing)")
    print(f"\nIssues included:")
    print(f"  - Inconsistent department casing/spacing")
    print(f"  - Null salaries (NaN)")
    print(f"  - Invalid performance ratings (<0 or >5)")
    print(f"  - Invalid hire dates (future, pre-2015, impossible dates)")
    print(f"  - Mixed date formats (DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD)")

    return data


def generate_cleaned_sample(input_file='uncleaned_dataset.csv', output_file='cleaned_dataset.csv'):
    """
    Create a sample cleaned version (without running the actual cleaning pipeline)
    This is for demonstration purposes so users can see expected output format
    """

    headers = [
        'EmpID', 'Department', 'Gender', 'Age', 'Salary',
        'Training_Hours', 'Performance_Rating', 'Years_Experience',
        'Employment_Status', 'Hire_Date'
    ]

    # Generate clean sample data
    clean_data = []
    for emp_id in range(1, 51):
        record = generate_employee_record(emp_id, include_issues=False)
        clean_data.append(record)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(clean_data)

    print(f"\nGenerated sample cleaned data in '{output_file}'")
    print(f"  - 50 clean records with ISO format dates")


if __name__ == "__main__":
    print("=" * 70)
    print("FAKE HR DATA GENERATOR")
    print("=" * 70)
    print("\nGenerating dataset with intentional data quality issues...\n")

    # Generate the main dataset
    generate_dataset(num_records=200, output_file='uncleaned_dataset.csv')

    # Generate a sample cleaned dataset for reference
    generate_cleaned_sample()

    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Run: python ../src/cleaner.py")
    print("2. Run: python ../src/metrics.py")
    print("\nYour code should handle:")
    print("  - NaN salary values")
    print("  - Mixed case departments")
    print("  - Out-of-range performance ratings")
    print("  - Mixed date formats and invalid dates")
