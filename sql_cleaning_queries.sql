-- =============================================
-- DATA CLEANING QUERIES FOR MAINTENANCE DATA
-- Based on HR analytics cleaning logic (cleaner.py)
-- Adapted for industrial equipment maintenance context
-- =============================================

-- =============================================
-- PART 1: DATA CLEANING (Mirrors cleaner.py)
-- =============================================

-- 1. REMOVE NULL/INVALID SENSOR READINGS
-- (Mirrors: remove_null_salaries)
DELETE FROM maintenance_records
WHERE sensor_value IS NULL 
   OR downtime_minutes IS NULL;

-- 2. STANDARDIZE COMPONENT NAMES
-- (Mirrors: standardize_departments)
UPDATE maintenance_records
SET component_name = LOWER(TRIM(component_name));

-- 3. REMOVE INVALID MTBF RANGES
-- (Mirrors: remove_invalid_performance_ratings)
DELETE FROM maintenance_records
WHERE mtbf_hours < 0 
   OR mtbf_hours > 10000;

-- 4. FIX DATE FORMATS TO YYYY-MM-DD
-- (Mirrors: fix_format_dates)
UPDATE maintenance_records
SET maintenance_date = STR_TO_DATE(maintenance_date, '%d/%m/%Y')
WHERE maintenance_date LIKE '%/%/%';

-- 5. VALIDATE DATE RANGES (2015-2025)
-- (Mirrors: remove_invalid_dates)
DELETE FROM maintenance_records
WHERE YEAR(maintenance_date) < 2015 
   OR YEAR(maintenance_date) > 2025;

-- 6. CHECK FOR LEAP YEAR / INVALID DATES
-- (Mirrors: leap year logic)
DELETE FROM maintenance_records
WHERE MONTH(maintenance_date) = 2 
   AND DAY(maintenance_date) = 29
   AND (YEAR(maintenance_date) % 4 != 0 
        OR (YEAR(maintenance_date) % 100 = 0 
            AND YEAR(maintenance_date) % 400 != 0));

-- =============================================
-- PART 2: METRICS CALCULATION (Mirrors metrics.py)
-- =============================================

-- 7. EQUIPMENT UPTIME (Retention rate equivalent)
SELECT 
    ROUND((COUNT(CASE WHEN status = 'Operational' THEN 1 END) * 100.0 / COUNT(*)), 2) AS uptime_percentage
FROM maintenance_records;

-- 8. FAILURE RATE BY EQUIPMENT TYPE (Turnover equivalent)
SELECT 
    component_name,
    COUNT(*) AS total_records,
    ROUND((SUM(CASE WHEN failure_occurred = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS failure_rate_percentage
FROM maintenance_records
GROUP BY component_name
ORDER BY failure_rate_percentage DESC;

-- 9. AVERAGE MTBF BY EQUIPMENT CATEGORY
-- (Mirrors: get_avg_age_by_department)
SELECT 
    equipment_category,
    ROUND(AVG(mtbf_hours), 2) AS avg_mtbf_hours,
    COUNT(*) AS number_of_failures
FROM maintenance_records
GROUP BY equipment_category
ORDER BY avg_mtbf_hours DESC;

-- 10. AVERAGE DOWNTIME FOR SPECIFIC DATE RANGE
-- (Mirrors: get_avg_salary_by_age_range)
SELECT 
    ROUND(AVG(downtime_minutes), 2) AS avg_downtime_minutes
FROM maintenance_records
WHERE maintenance_date BETWEEN '2024-01-01' AND '2024-12-31';

-- 11. PERFORMANCE VS MAINTENANCE HOURS
-- (Mirrors: get_avg_dept_performance_by_training_range)
SELECT 
    component_name,
    ROUND(AVG(performance_score), 2) AS avg_performance,
    ROUND(AVG(maintenance_hours), 2) AS avg_maintenance_hours,
    COUNT(*) AS maintenance_events
FROM maintenance_records
WHERE maintenance_hours BETWEEN 20 AND 40
GROUP BY component_name
ORDER BY avg_performance DESC;
