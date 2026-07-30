-- Check Tables
SELECT table_name
FROM user_tables
ORDER BY table_name;


-- Check Table Structure
DESC SUPPLIER;

DESC ITEM;

DESC SALES;


-- Check Constraints
SELECT
    constraint_name,
    constraint_type,
    table_name,
    status
FROM user_constraints
WHERE table_name IN ('SUPPLIER', 'ITEM', 'SALES')
ORDER BY table_name, constraint_type;


-- Check Primary Keys
SELECT
    cols.table_name,
    cols.column_name,
    cons.constraint_name
FROM user_constraints cons
JOIN user_cons_columns cols
ON cons.constraint_name = cols.constraint_name
WHERE cons.constraint_type = 'P'
ORDER BY cols.table_name;


-- Check Foreign Keys
SELECT
    a.table_name,
    a.column_name,
    a.constraint_name,
    c_pk.table_name AS referenced_table
FROM user_cons_columns a
JOIN user_constraints c
ON a.constraint_name = c.constraint_name
JOIN user_constraints c_pk
ON c.r_constraint_name = c_pk.constraint_name
WHERE c.constraint_type = 'R'
ORDER BY a.table_name;


-- Check Row Counts
SELECT 'SUPPLIER' AS TABLE_NAME, COUNT(*) AS ROW_COUNT
FROM SUPPLIER

UNION ALL

SELECT 'ITEM', COUNT(*)
FROM ITEM

UNION ALL

SELECT 'SALES', COUNT(*)
FROM SALES;