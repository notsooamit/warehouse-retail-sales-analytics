-- ==========================================
-- PRODUCT ANALYTICS 1
-- Top Selling Products
-- ==========================================

SELECT

    ITEM_CODE,
    ITEM_DESCRIPTION,
    ITEM_TYPE,

    TOTAL_SALES

FROM VW_PRODUCT_PERFORMANCE

ORDER BY TOTAL_SALES DESC

FETCH FIRST 20 ROWS ONLY;

-- ==========================================
-- PRODUCT ANALYTICS 2
-- Lowest Selling Products
-- ==========================================

SELECT

    ITEM_CODE,
    ITEM_DESCRIPTION,
    ITEM_TYPE,

    TOTAL_SALES

FROM VW_PRODUCT_PERFORMANCE

ORDER BY TOTAL_SALES

FETCH FIRST 20 ROWS ONLY;

-- ==========================================
-- PRODUCT ANALYTICS 3
-- Sales by Product Category
-- ==========================================

SELECT

    ITEM_TYPE,

    SUM(TOTAL_SALES) AS TOTAL_SALES

FROM VW_PRODUCT_PERFORMANCE

GROUP BY ITEM_TYPE

ORDER BY TOTAL_SALES DESC;

-- ==========================================
-- PRODUCT ANALYTICS 4
-- Product Count by Category
-- ==========================================

SELECT

    ITEM_TYPE,

    COUNT(*) AS PRODUCT_COUNT

FROM ITEM

GROUP BY ITEM_TYPE

ORDER BY PRODUCT_COUNT DESC;

-- ==========================================
-- PRODUCT ANALYTICS 5
-- Average Sales per Product
-- ==========================================

SELECT

    ITEM_TYPE,

    ROUND(
        AVG(TOTAL_SALES),
        2
    ) AS AVERAGE_PRODUCT_SALES

FROM VW_PRODUCT_PERFORMANCE

GROUP BY ITEM_TYPE

ORDER BY AVERAGE_PRODUCT_SALES DESC;

-- ==========================================
-- PRODUCT ANALYTICS 6
-- Products with No Retail Sales
-- ==========================================

SELECT

    ITEM_CODE,
    ITEM_DESCRIPTION,
    ITEM_TYPE

FROM VW_PRODUCT_PERFORMANCE

WHERE NVL(TOTAL_RETAIL_SALES, 0) = 0

ORDER BY ITEM_DESCRIPTION;

-- ==========================================
-- PRODUCT ANALYTICS 7
-- Products with No Warehouse Sales
-- ==========================================

SELECT

    ITEM_CODE,
    ITEM_DESCRIPTION,
    ITEM_TYPE

FROM VW_PRODUCT_PERFORMANCE

WHERE NVL(TOTAL_WAREHOUSE_SALES, 0) = 0

ORDER BY ITEM_DESCRIPTION;