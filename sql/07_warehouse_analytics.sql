-- ==========================================
-- WAREHOUSE ANALYTICS 1
-- Warehouse vs Retail Sales
-- ==========================================

SELECT

    YEAR,
    MONTH,

    TOTAL_RETAIL_SALES,
    TOTAL_WAREHOUSE_SALES

FROM VW_MONTHLY_SALES

ORDER BY
    YEAR,
    MONTH;

-- ==========================================
-- WAREHOUSE ANALYTICS 2
-- Warehouse Contribution
-- ==========================================

SELECT

    YEAR,
    MONTH,

    ROUND(
        TOTAL_WAREHOUSE_SALES /
        TOTAL_SALES * 100,
        2
    ) AS WAREHOUSE_PERCENT

FROM VW_MONTHLY_SALES

ORDER BY
    YEAR,
    MONTH;

-- ==========================================
-- WAREHOUSE ANALYTICS 3
-- Top Suppliers by Warehouse Sales
-- ==========================================

SELECT

    SUPPLIER_NAME,

    TOTAL_WAREHOUSE_SALES

FROM VW_SUPPLIER_PERFORMANCE

ORDER BY TOTAL_WAREHOUSE_SALES DESC;

-- ==========================================
-- WAREHOUSE ANALYTICS 4
-- Warehouse Sales by Item Type
-- ==========================================

SELECT

    ITEM_TYPE,

    SUM(TOTAL_WAREHOUSE_SALES) AS TOTAL_WAREHOUSE_SALES

FROM VW_PRODUCT_PERFORMANCE

GROUP BY ITEM_TYPE

ORDER BY TOTAL_WAREHOUSE_SALES DESC;

-- ==========================================
-- WAREHOUSE ANALYTICS 5
-- Top Warehouse Products
-- ==========================================

SELECT

    ITEM_CODE,
    ITEM_DESCRIPTION,

    TOTAL_WAREHOUSE_SALES

FROM VW_PRODUCT_PERFORMANCE

ORDER BY TOTAL_WAREHOUSE_SALES DESC

FETCH FIRST 20 ROWS ONLY;

-- ==========================================
-- WAREHOUSE ANALYTICS 6
-- Retail vs Warehouse Comparison
-- ==========================================

SELECT

    ITEM_DESCRIPTION,

    TOTAL_RETAIL_SALES,

    TOTAL_WAREHOUSE_SALES

FROM VW_PRODUCT_PERFORMANCE

ORDER BY TOTAL_WAREHOUSE_SALES DESC;