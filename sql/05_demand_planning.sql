-- ==========================================
-- DEMAND PLANNING 1
-- Monthly Sales Trend
-- ==========================================

SELECT

    YEAR,
    MONTH,

    TOTAL_RETAIL_SALES,
    TOTAL_WAREHOUSE_SALES,
    TOTAL_SALES

FROM VW_MONTHLY_SALES

ORDER BY
    YEAR,
    MONTH;

-- ==========================================
-- DEMAND PLANNING 2
-- Highest Sales Months
-- ==========================================

SELECT

    YEAR,
    MONTH,

    TOTAL_SALES

FROM VW_MONTHLY_SALES

ORDER BY TOTAL_SALES DESC;


-- ==========================================
-- DEMAND PLANNING 3
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
-- DEMAND PLANNING 4
-- Sales by Item Type
-- ==========================================

SELECT

    ITEM_TYPE,

    SUM(TOTAL_SALES) AS TOTAL_SALES

FROM VW_PRODUCT_PERFORMANCE

GROUP BY ITEM_TYPE

ORDER BY TOTAL_SALES DESC;


-- ==========================================
-- DEMAND PLANNING 5
-- Lowest Selling Products
-- ==========================================

SELECT

    ITEM_CODE,
    ITEM_DESCRIPTION,

    TOTAL_SALES

FROM VW_PRODUCT_PERFORMANCE

ORDER BY TOTAL_SALES

FETCH FIRST 20 ROWS ONLY;


-- ==========================================
-- DEMAND PLANNING 6
-- Product Contribution %
-- ==========================================

SELECT

    ITEM_CODE,
    ITEM_DESCRIPTION,

    TOTAL_SALES,

    ROUND(
        TOTAL_SALES /
        SUM(TOTAL_SALES) OVER () * 100,
        2
    ) AS SALES_PERCENTAGE

FROM VW_PRODUCT_PERFORMANCE

ORDER BY TOTAL_SALES DESC;