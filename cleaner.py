import math
from datetime import datetime
from helper import read_hr_data  

def remove_null_salaries(data):
    """
    Remove all records where Salary (index 4) is NaN or missing.
    """
    #We created the list that will store only the valid employee records.
    cleaned_data = []

    #The code here then Loops through each employee record in the dataset.
    for row in data:
        #We then create a salary value is stored at index 4.
        salary = row[4]

        #The code will then check if the salary is not NaN
        if not math.isnan(salary):
            #If salary is valid,keep the record.
            cleaned_data.append(row)

    #The code will then return the cleaned dataset.
    return cleaned_data


def standardize_departments(data):
    """
    Convert all Department names (index 1) to lowercase.
    """
    #Here we loop through each employee record.
    for row in data:
        #Continue to remove extra spaces and convert department name to .lowercase.
        row[1] = row[1].strip().lower()


def remove_invalid_performance_ratings(data):
    """
    Remove records with Performance_Rating (index 6) outside range [0, 5].
    """
    #This list will then store only records with valid ratings.
    cleaned_data = []

    #we then Loop through the dataset.
    for row in data:
        #Performance rating is stored at index 6.
        rating = row[6]

        #Keep the rating only if it is between 0 and 5 (+1,inclusive).
        if 0 <= rating <= 5:
            cleaned_data.append(row)

    #Here we return the cleaned dataset.
    return cleaned_data


def fix_format_dates(data):
    """
    Fix Hire_Date (index 9) format.
    """
    #The code will then Loop through each employee record.
    for row in data:
        #Get the hire date and  the leading/trailing spaces thereafter.
        date_str = row[9].strip()

        #Check if the date is in DD/MM/YYYY format.
        if "/" in date_str:
            try:
                #Convert the string to a datetime object
                date_obj = datetime.strptime(date_str, "%d/%m/%Y")

                #Convert the date to YYYY-MM-DD format
                row[9] = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                #If conversion fails,we ignore the date for now.
                pass


def remove_invalid_dates(data):
    """
    Remove invalid Hire_Date entries(index 9).
    """
    #This list will store only records with valid dates.
    cleaned_data = []

    #Here we then effectively Loop through the dataset.
    for row in data:
        #Get and clean the hire date string.
        date_str = row[9].strip()

        try:
            #Here we try converting the date string to a datetime object.
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            year = date_obj.year
            month = date_obj.month
            day = date_obj.day

            #Then remove dates before company founding or far in the future.
            if year < 2015 or year > 2025:
                continue

            #Then we validate month range.
            if month < 1 or month > 12:
                continue

            #Handle February separately because of leap years.
            if month == 2:
                #Check if the year is a leap year.
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    if day < 1 or day > 29:
                        continue
                else:
                    if day < 1 or day > 28:
                        continue
            else:
                #All other months have a maximum of 30 days.
                if day < 1 or day > 30:
                    continue

            #If all checks pass,then we noted to keep the record.
            cleaned_data.append(row)

        except ValueError:
            #Invalid date formats or impossible dates are removed.
            continue

    #Return the cleaned dataset.
    return cleaned_data


if __name__ == "__main__":
    #Load the uncleaned data from the CSV file
    data = read_hr_data('uncleaned_dataset.csv')
    print(f"Loaded {len(data)} employee records\n")

    print("=" * 70)
    print("DATA CLEANING")
    print("=" * 70)

    #Test data cleaning functions
    #You can comment or uncomment these lines as needed

    #1.Remove records with null salaries
    removed_salaries = remove_null_salaries(data)
    print(f"Removed {len(removed_salaries)} records with null salaries")
    print(f"Remaining records: {len(data)}\n")

    #2.Standardise department names
    standardize_departments(data)
    print("Standardised department names to lowercase\n")

    #3.Remove invalid performance ratings
    removed_ratings = remove_invalid_performance_ratings(data)
    print(f"Removed {len(removed_ratings)} records with invalid performance ratings")
    print(f"Remaining records: {len(data)}\n")

    #4.Fix hire date formatting
    fix_format_dates(data)
    print("Fixed hire date formatting\n")

    #5.Remove invalid hire dates
    removed_dates = remove_invalid_dates(data)
    print(f"Removed {len(removed_dates)} records with invalid dates")
    print(f"Remaining records: {len(data)}\n")
