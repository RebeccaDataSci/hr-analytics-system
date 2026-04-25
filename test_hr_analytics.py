
from metrics import get_retention_rate, get_turnover_rate_by_department
from cleaner import remove_null_salaries, remove_invalid_performance_ratings, remove_invalid_dates
import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


# Sample test data
sample_data = [
    [1, "engineering", "Male", 30, 50000, 40, 4, 5, "Active", "2020-01-15"],
    [2, "sales", "Female", 25, float(
        'nan'), 20, 3, 2, "Resigned", "2022-03-10"],
    [3, "HR", "Female", 35, 60000, 50, 6, 8,
        "Active", "2018-07-22"],  # Invalid rating 6
]


def test_remove_null_salaries():
    result = remove_null_salaries(sample_data)
    # Should remove record 2 (null salary)
    assert len(result) == 2
    assert result[0][0] == 1
    assert result[1][0] == 3


def test_remove_invalid_performance_ratings():
    result = remove_invalid_performance_ratings(sample_data)
    # Should remove record 3 (rating 6 > 5)
    assert len(result) == 2
    assert result[0][6] == 4  # rating 4
    assert result[1][6] == 3  # rating 3


def test_retention_rate():
    rate = get_retention_rate(sample_data)
    # 2 out of 3 employees are Active (66.67%)
    assert rate == 66.67


def test_turnover_rate():
    rates = get_turnover_rate_by_department(sample_data)
    # Sales: 1 resigned out of 1 = 100%
    assert rates["sales"] == 100.0
    # Engineering: 0 resigned out of 1 = 0%
    assert rates["engineering"] == 0.0
