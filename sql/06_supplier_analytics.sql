-- ==========================================
-- SUPPLIER ANALYTICS 1
-- Top Suppliers by Total Sales
-- ==========================================

SELECT

    SUPPLIER_ID,
    SUPPLIER_NAME,

    TOTAL_RETAIL_SALES,
    TOTAL_WAREHOUSE_SALES,
    TOTAL_SALES

FROM VW_SUPPLIER_PERFORMANCE

ORDER BY TOTAL_SALES DESC;


-- ==========================================
-- SUPPLIER ANALYTICS 2
-- Top 10 Suppliers
-- ==========================================

SELECT

    SUPPLIER_NAME,
    TOTAL_SALES

FROM VW_SUPPLIER_PERFORMANCE

ORDER BY TOTAL_SALES DESC

FETCH FIRST 10 ROWS ONLY;

-- ==========================================
-- SUPPLIER ANALYTICS 3
-- Supplier Product Portfolio
-- ==========================================

SELECT

    SUPPLIER_NAME,
    PRODUCT_COUNT

FROM VW_SUPPLIER_PERFORMANCE

ORDER BY PRODUCT_COUNT DESC;

-- ==========================================
-- SUPPLIER ANALYTICS 4
-- Supplier Contribution %
-- ==========================================

SELECT

    SUPPLIER_NAME,

    TOTAL_SALES,

    ROUND(
        TOTAL_SALES /
        SUM(TOTAL_SALES) OVER () * 100,
        2
    ) AS CONTRIBUTION_PERCENT

FROM VW_SUPPLIER_PERFORMANCE

ORDER BY TOTAL_SALES DESC;

-- ==========================================
-- SUPPLIER ANALYTICS 5
-- Supplier Ranking
-- ==========================================

SELECT

    RANK() OVER (
        ORDER BY TOTAL_SALES DESC
    ) AS SUPPLIER_RANK,

    SUPPLIER_NAME,

    TOTAL_SALES

FROM VW_SUPPLIER_PERFORMANCE

ORDER BY SUPPLIER_RANK;

-- ==========================================
-- SUPPLIER ANALYTICS 6
-- Above Average Suppliers
-- ==========================================

SELECT

    SUPPLIER_NAME,

    TOTAL_SALES

FROM VW_SUPPLIER_PERFORMANCE

WHERE TOTAL_SALES >
(
    SELECT AVG(TOTAL_SALES)
    FROM VW_SUPPLIER_PERFORMANCE
)

ORDER BY TOTAL_SALES DESC;

-- ==========================================
-- SUPPLIER ANALYTICS 7
-- Retail vs Warehouse Sales
-- ==========================================

SELECT

    SUPPLIER_NAME,

    TOTAL_RETAIL_SALES,

    TOTAL_WAREHOUSE_SALES

FROM VW_SUPPLIER_PERFORMANCE

ORDER BY TOTAL_SALES DESC;