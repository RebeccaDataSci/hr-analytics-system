import math
from datetime import datetime
from helper import read_hr_data

def get_unique_departments(data):
    """
    Return a set of all unique department names in the dataset.
    
    Args:
        data (list): 2D list of employee records
        
    Returns:
        set: Set of department names
        
    Example:
        >>> get_unique_departments(data)
        {'engineering', 'sales', 'hr', 'marketing', 'product'}
    """
    #Here we created an empty set to store departments because we are aware that sets remove duplicates.
    departments = set()

    #The code then goes through each employee record in the data using the for loop.
    for row in data:
        #The department name is then stored at index 1.
        departments.add(row[1])

    #Return is then the final set of unique department names, as the required output.
    return departments


def get_gender_distribution(data):
    """
    Return gender distribution (as percentages) for each department.
    
    All percentages should be rounded to 2 decimal places.
    """
    #The dictionary will store gender counts and later the actual percentages.
    result = {}

    #Here the code then Loops through each employee record.
    for row in data:
        dept = row[1]
        gender = row[2]

        #If the department is not yet in the dictionary, we then add it here.
        if dept not in result:
            result[dept] = {}

        #If the gender has not yet been counted, the code here starts from 0.
        if gender not in result[dept]:
            result[dept][gender] = 0

        #This part of the code then will increase the count for the gender.
        result[dept][gender] += 1

    #It will then Convert the counts to percentages(%).
    for dept in result:
        #Here the code will sum to get the total number of employees in the department.
        total = sum(result[dept].values())

        for gender in result[dept]:
            percentage = (result[dept][gender] / total) * 100
            result[dept][gender] = round(percentage, 2)

    return result


def get_avg_age_by_department(data):
    """
    Return average age for each department.
    """
    #The Dictionaries are to track total ages and employee counts.
    totals = {}
    counts = {}

    #The code then Loops through each employee record.
    for row in data:
        dept = row[1]
        age = row[3]

        #It then Initialise's values for new the departments.
        if dept not in totals:
            totals[dept] = 0
            counts[dept] = 0

        #The code then add's age and increases the count.
        totals[dept] += age
        counts[dept] += 1

    #It will then Calculate the average age per department.
    result = {}
    for dept in totals:
        average = totals[dept] / counts[dept]
        result[dept] = round(average, 2)

    return result


def get_retention_rate(data):
    """
    Calculate overall retention rate as a percentage.
    """
    total_employees = len(data)
    active_employees = 0

    #Here we count how many employees are marked as active.
    for row in data:
        if row[8] == "Active":
            active_employees += 1

    #Then the code will basically calculate retention percentage.
    retention_rate = (active_employees / total_employees) * 100
    return round(retention_rate, 2)


def get_turnover_rate_by_department(data):
    """
    Calculate turnover rate for each department as a percentage.
    """
    total = {}
    resigned = {}

    #It then Loops through all employee records.
    for row in data:
        dept = row[1]
        status = row[8]

        #Initialise's the department values if not present.
        if dept not in total:
            total[dept] = 0
            resigned[dept] = 0

        total[dept] += 1

        #We can then Count the resigned employees.
        if status == "Resigned":
            resigned[dept] += 1

    #The turnover rate is calculated per department.
    result = {}
    for dept in total:
        rate = (resigned[dept] / total[dept]) * 100
        result[dept] = round(rate, 2)

    return result


def get_avg_salary_by_age_range(data, min_age, max_age):
    """
    Return average salary for employees within an age range (inclusive).
    """
    salaries = []

    #We then effectively collect salaries of employees in the age range.
    for row in data:
        age = row[3]
        salary = row[4]

        if min_age <= age <= max_age:
            salaries.append(salary)

    #If no employees fall in the age range, return 0 instead of dividing by zero
    if len(salaries) == 0:
        return 0.0

    #Here we calculate the average salary.
    average_salary = sum(salaries) / len(salaries)
    return round(average_salary, 2)


def get_avg_dept_performance_by_training_range(data, min_hours, max_hours):
    """
    Return average performance rating for each department within a training hours range (inclusive).
    """
    totals = {}
    counts = {}

    #We then Loop through each of the employee records.
    for row in data:
        dept = row[1]
        training_hours = row[5]
        rating = row[6]

        #Only included the employees whose training hours are in range.
        if min_hours <= training_hours <= max_hours:
            if dept not in totals:
                totals[dept] = 0
                counts[dept] = 0

            totals[dept] += rating
            counts[dept] += 1

    #The code here then calculate's average performance rating per department.
    result = {}
    for dept in totals:
        average = totals[dept] / counts[dept]
        result[dept] = round(average, 2)

    return result


if __name__ == "__main__":
    #Load cleaned data from CSV file
    data = read_hr_data('cleaned_dataset.csv')
    print(f"Loaded {len(data)} employee records\n")
    
    print("=" * 70)
    print("METRICS CALCULATION")
    print("=" * 70)
    
    #1. Get unique departments
    depts = get_unique_departments(data)
    print(f"\n1. Unique departments: {depts}")
    
    #2. Get gender distribution per department
    gender_dist = get_gender_distribution(data)
    print(f"\n2. Gender distribution per department:")
    for dept, dist in gender_dist.items():
        print(f"  {dept}: {dist}")
    
    #3. Get average age per department
    avg_age = get_avg_age_by_department(data)
    print(f"\n3. Average age per department:")
    for dept, age in avg_age.items():
        print(f"  {dept}: {age}")
    
    #4. Get retention rate
    retention = get_retention_rate(data)
    print(f"\n4. Overall retention rate: {retention}%")
    
    #5. Get turnover rate per department
    turnover = get_turnover_rate_by_department(data)
    print(f"\n5. Turnover rate per department:")
    for dept, rate in turnover.items():
        print(f"  {dept}: {rate}%")
    
    #6. Get average salary for age range
    avg_sal_age = get_avg_salary_by_age_range(data, 25, 35)
    print(f"\n6. Average salary for age range: {avg_sal_age}")
    
    #7. Get average department performance by training hours range
    avg_perf_training = get_avg_dept_performance_by_training_range(data, 20, 40)
    print(f"\n7. Average department performance by training hours range:")
    for dept, rating in avg_perf_training.items():
        print(f"  {dept}: {rating}")