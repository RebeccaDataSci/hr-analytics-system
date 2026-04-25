
import csv


def read_hr_data(filename):
    """
    Read HR data from CSV file, return as list of lists.
    Converts numeric fields to appropriate types.
    """
    data = []
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip header row

            for row in reader:
                # Convert fields to correct types
                # Row structure: EmpID, Dept, Gender, Age, Salary, Training_Hours,
                # Performance_Rating, Years_Experience, Employment_Status, Hire_Date

                emp_id = int(row[0]) if row[0] else 0
                department = row[1]
                gender = row[2]

                # Handle age (may be empty or invalid)
                try:
                    age = int(row[3]) if row[3] else 0
                except ValueError:
                    age = 0

                # Handle salary (may be NaN as string)
                try:
                    salary = float(row[4]) if row[4] and row[4].lower(
                    ) != 'nan' else float('nan')
                except ValueError:
                    salary = float('nan')

                # Training hours
                try:
                    training_hours = int(row[5]) if row[5] else 0
                except ValueError:
                    training_hours = 0

                # Performance rating
                try:
                    performance_rating = int(row[6]) if row[6] else 0
                except ValueError:
                    performance_rating = 0

                # Years of experience
                try:
                    years_experience = int(row[7]) if row[7] else 0
                except ValueError:
                    years_experience = 0

                employment_status = row[8]
                hire_date = row[9] if len(row) > 9 else ""

                data.append([emp_id, department, gender, age, salary,
                             training_hours, performance_rating, years_experience,
                             employment_status, hire_date])
    except FileNotFoundError:
        print(
            f"Error: File '{filename}' not found. Run data/generate_fake_hr_data.py first.")
        return []

    return data
