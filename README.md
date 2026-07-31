# Warehouse & Retail Sales Analytics

An end-to-end **ETL pipeline** that extracts 319,000+ retail and warehouse sales records from CSV, transforms and normalizes them into a 3NF relational schema in Oracle, and delivers business intelligence through SQL analytics and Power BI dashboards.

**Tech Stack:** Python · Pandas · Oracle XE · SQL · Power BI

---

## Dashboard Preview

![Executive Sales Dashboard](dashboard/screenshots/01_executive_overview.png)

**Key findings from the analysis:**
- Total revenue of **$10.35M** across all channels and time periods
- **78% of sales flow through the warehouse channel** ($8.12M) vs 22% retail ($2.23M), indicating a wholesale-dominant distribution model
- Crown Imports leads supplier revenue at $1.84M, followed by Miller Brewing and Anheuser-Busch
- Clear seasonal demand patterns visible in the monthly trend — useful for demand forecasting and inventory planning

---

## Table of Contents

- [Architecture](#architecture)
- [ETL Pipeline](#etl-pipeline)
- [Database Schema](#database-schema)
- [SQL Analytics Layer](#sql-analytics-layer)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [How to Run](#how-to-run)
- [Technical Notes](#technical-notes)

---

## Architecture

The project follows a layered architecture with clear separation between data processing, storage, and analytics:

```
┌────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                        │
│   Power BI Dashboard · Executive KPIs · Analytics Reports    │
├────────────────────────────────────────────────────────────────┤
│                     ANALYTICS LAYER (SQL)                      │
│   Demand Planning · Supplier · Warehouse · Product Analytics  │
├────────────────────────────────────────────────────────────────┤
│                     VIEW LAYER (SQL)                           │
│   VW_SALES_DETAILS · VW_MONTHLY_SALES                         │
│   VW_SUPPLIER_PERFORMANCE · VW_PRODUCT_PERFORMANCE            │
│   VW_DISTRIBUTION_ANALYSIS                                     │
├────────────────────────────────────────────────────────────────┤
│                     STORAGE LAYER (Oracle)                     │
│   SUPPLIER (PK) ──┐                                           │
│   ITEM (PK) ──────┼──→ SALES (FK, FK)                         │
├────────────────────────────────────────────────────────────────┤
│                     ETL LAYER (Python)                         │
│   Extract (CSV) → Explore → Clean → Normalize → Load (Oracle) │
├────────────────────────────────────────────────────────────────┤
│                     SOURCE LAYER                               │
│   sales.csv (319,029 rows · 34 MB)                             │
└────────────────────────────────────────────────────────────────┘
```

---

## ETL Pipeline

The pipeline executes in five sequential stages:

```
 ╔══════════╗     ╔══════════╗     ╔══════════╗     ╔═════════════╗     ╔══════════╗
 ║ EXTRACT  ║ ──→ ║ EXPLORE  ║ ──→ ║  CLEAN   ║ ──→ ║  NORMALIZE  ║ ──→ ║   LOAD   ║
 ║ CSV Read ║     ║ Profiling║     ║ Transform║     ║  3NF Split  ║     ║  Oracle  ║
 ╚══════════╝     ╚══════════╝     ╚══════════╝     ╚═════════════╝     ╚══════════╝
```

### Stage 1 — Extract

Reads the raw CSV file (319,029 rows × 9 columns) into a Pandas DataFrame.

### Stage 2 — Explore

Data profiling to assess quality before transformation:

| Report | Purpose |
|--------|---------|
| Dataset Summary | Row/column count, data types, memory usage |
| Missing Values | Per-column null counts and percentages |
| Distinct Values | Unique value counts per column |
| Duplicate Report | Full-row duplicate detection |
| Special Characters | Accounting negatives `(1,234)`, commas, blanks, invalid characters |
| Key Consistency | Validates whether ITEM CODE maps to a single DESCRIPTION, TYPE, and SUPPLIER |

### Stage 3 — Clean

Transforms sales columns from raw text to numeric values:

| Raw Value | Transformation | Result |
|-----------|---------------|--------|
| `1,234.56` | Remove commas | `1234.56` |
| `(500)` | Accounting negative | `-500.0` |
| ` ` (blank) | Blank to NaN | `NaN` |
| `abc` | Invalid to NaN | `NaN` |

Post-cleaning validation confirms all sales columns are numeric with no residual formatting characters.

### Stage 4 — Normalize

Decomposes the flat CSV into **Third Normal Form (3NF)**:

```
                    ┌──────────────────┐
                    │    sales.csv     │
                    │   (flat file)    │
                    └────────┬─────────┘
                             │
               ┌─────────────┼─────────────┐
               ▼             ▼             ▼
      ┌──────────────┐ ┌──────────┐ ┌──────────────┐
      │   SUPPLIER   │ │   ITEM   │ │    SALES     │
      │──────────────│ │──────────│ │──────────────│
      │ SUPPLIER_ID  │ │ ITEM_CODE│ │ YEAR         │
      │ SUPPLIER_NAME│ │ ITEM_DESC│ │ MONTH        │
      └──────┬───────┘ │ ITEM_TYPE│ │ ITEM_CODE(FK)│
             │         └────┬─────┘ │ SUPPLIER_ID  │
             │              │       │   (FK)       │
             └──────────────┴───────│ RETAIL_SALES │
                      referenced by │ RETAIL_TRANS │
                                    │ WAREHOUSE    │
                                    └──────────────┘
```

Validation checks after normalization confirm no duplicate primary keys and no missing foreign keys.

### Stage 5 — Load

Inserts normalized DataFrames into Oracle using `python-oracledb`. Handles `NaN` to `None` conversion for nullable columns, uses `executemany()` for batch inserts, and loads in dependency order: SUPPLIER → ITEM → SALES.

---

## Database Schema

### Entity-Relationship Diagram

```
┌──────────────────────┐          ┌──────────────────────────────────┐
│      SUPPLIER        │          │              SALES               │
│──────────────────────│          │──────────────────────────────────│
│ * SUPPLIER_ID  (PK)  │─────┐   │   YEAR             NUMBER  (NN) │
│   SUPPLIER_NAME      │     │   │   MONTH            NUMBER  (NN) │
│   VARCHAR2(200)      │     ├──→│ * SUPPLIER_ID (FK)  NUMBER  (NN) │
└──────────────────────┘     │   │ * ITEM_CODE   (FK)  VARCHAR (NN) │
                             │   │   RETAIL_SALES      NUMBER(12,2) │
┌──────────────────────┐     │   │   RETAIL_TRANSFERS  NUMBER(12,2) │
│        ITEM          │     │   │   WAREHOUSE_SALES   NUMBER(12,2) │
│──────────────────────│     │   └──────────────────────────────────┘
│ * ITEM_CODE    (PK)  │─────┘
│   ITEM_DESCRIPTION   │            PK = Primary Key
│   VARCHAR2(300)      │            FK = Foreign Key
│   ITEM_TYPE          │            NN = NOT NULL
│   VARCHAR2(50)       │
└──────────────────────┘
```

### Constraints

| Constraint | Type | Table | Column(s) |
|------------|------|-------|-----------|
| PK_SUPPLIER | Primary Key | SUPPLIER | SUPPLIER_ID |
| PK_ITEM | Primary Key | ITEM | ITEM_CODE |
| FK_SALES_SUPPLIER | Foreign Key | SALES | SUPPLIER_ID → SUPPLIER |
| FK_SALES_ITEM | Foreign Key | SALES | ITEM_CODE → ITEM |

---

## SQL Analytics Layer

### Business Views

Five views power the analytics and dashboard layer:

| View | Purpose |
|------|---------|
| `VW_SALES_DETAILS` | Denormalized join of all 3 tables — full row-level detail |
| `VW_MONTHLY_SALES` | Monthly aggregated totals with retail, warehouse, and combined sales |
| `VW_SUPPLIER_PERFORMANCE` | Supplier-level KPIs including product count and sales breakdown |
| `VW_PRODUCT_PERFORMANCE` | Product-level retail vs warehouse performance |
| `VW_DISTRIBUTION_ANALYSIS` | Retail transfer activity and distribution patterns |

`TOTAL_SALES` is defined as `RETAIL_SALES + WAREHOUSE_SALES`. RETAIL_TRANSFERS represent inventory movement between stores and are excluded from the revenue total.

### Analytics Domains

| Domain | Script | Queries | Key Analyses |
|--------|--------|---------|-------------|
| Demand Planning | `05_demand_planning.sql` | 6 | Monthly trends, peak months, top/bottom products, contribution % |
| Supplier Analytics | `06_supplier_analytics.sql` | 7 | Ranking, portfolio size, contribution %, above-average suppliers |
| Warehouse Analytics | `07_warehouse_analytics.sql` | 6 | Warehouse contribution %, retail vs warehouse comparison |
| Product Analytics | `08_product_analytics.sql` | 7 | Category analysis, average sales per product, no-sales detection |
| Dashboard | `10_dashboard_queries.sql` | 8 | Executive KPIs, summary queries for Power BI |

### Dashboard Data Sources

| Power BI Page | Oracle View | Supply Chain Concepts |
|---------------|-------------|----------------------|
| Executive Overview | VW_MONTHLY_SALES, VW_SUPPLIER_PERFORMANCE, VW_PRODUCT_PERFORMANCE | S&OP, KPIs |
| Demand Planning | VW_MONTHLY_SALES, VW_PRODUCT_PERFORMANCE | Forecasting, ABC Segmentation |
| Supplier Analytics | VW_SUPPLIER_PERFORMANCE | Spend Analytics, Concentration Risk |
| Warehouse & SKU | VW_PRODUCT_PERFORMANCE, VW_MONTHLY_SALES | SKU Velocity, Throughput |
| Distribution | VW_DISTRIBUTION_ANALYSIS | DRP, Retail Transfers |

---

## Project Structure

```
Sales_ETL_Project/
│
├── main.py                        # ETL entry point — runs full pipeline
│
├── src/
│   ├── __init__.py
│   ├── config.py                  # File paths, column lists, DB credentials
│   ├── explore.py                 # Data profiling and exploration reports
│   ├── clean.py                   # Sales column cleaning and validation
│   ├── normalize.py               # 3NF decomposition (SUPPLIER, ITEM, SALES)
│   ├── oracle_loader.py           # Oracle connection and batch inserts
│   └── utils.py                   # Utility functions
│
├── data/
│   └── sales.csv                  # Source data (319,029 rows)
│
├── sql/
│   ├── 01_create_user.sql         # Database user setup
│   ├── 02_create_tables.sql       # Table DDL
│   ├── 03_constraints.sql         # PKs, FKs, NOT NULLs
│   ├── 04_validation.sql          # Schema verification queries
│   ├── 05_demand_planning.sql     # Demand planning analytics
│   ├── 06_supplier_analytics.sql  # Supplier performance analytics
│   ├── 07_warehouse_analytics.sql # Warehouse analytics
│   ├── 08_product_analytics.sql   # Product analytics
│   ├── 09_business_views.sql      # Business view definitions
│   └── 10_dashboard_queries.sql   # Dashboard KPI queries
│
├── dashboard/
│   └── screenshots/               # Power BI dashboard exports
│
├── requirements.txt               # Python dependencies
└── README.md
```

### Module Responsibilities

```
┌─────────────┐
│  main.py    │  Orchestrates the full ETL pipeline
└──────┬──────┘
       │ imports
       ▼
┌─────────────────────────────────────────────────┐
│                    src/                          │
│                                                 │
│  config.py ─────→ Constants & DB configuration  │
│       │                                         │
│       ▼                                         │
│  explore.py ────→ Extract + Data Profiling      │
│       │                                         │
│       ▼                                         │
│  clean.py ──────→ Data Cleaning & Validation    │
│       │                                         │
│       ▼                                         │
│  normalize.py ──→ 3NF Normalization             │
│       │                                         │
│       ▼                                         │
│  oracle_loader.py → Oracle Insert               │
└─────────────────────────────────────────────────┘
```

---

## Setup and Installation

### Prerequisites

- Python 3.8+
- Oracle Database XE (21c or later) with a Pluggable Database (`XEPDB1`)
- Power BI Desktop (for dashboard visualization)

### 1. Clone the Repository

```bash
git clone https://github.com/notsooamit/warehouse-retail-sales-analytics.git
cd warehouse-retail-sales-analytics
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Oracle Database

Run the SQL scripts in order using SQL*Plus or SQL Developer:

```sql
-- Connect as SYSDBA
@sql/01_create_user.sql

-- Connect as sales_etl
@sql/02_create_tables.sql
@sql/03_constraints.sql
```

### 4. Configure Connection

Update database credentials in `src/config.py`:

```python
DB_USER = "sales_etl"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = 1521
DB_SERVICE = "XEPDB1"
```

---

## How to Run

### Run the Full ETL Pipeline

```bash
python main.py
```

This will:
1. Load `data/sales.csv` into a DataFrame
2. Run data profiling reports (missing values, duplicates, special characters)
3. Clean sales columns (accounting negatives, commas, blanks)
4. Normalize into 3NF tables (SUPPLIER, ITEM, SALES)
5. Load all tables into Oracle

### Create Views and Run Analytics

After loading data, create the business views and execute analytics:

```sql
-- Connect as sales_etl
@sql/09_business_views.sql      -- Create views first
@sql/04_validation.sql          -- Verify data loaded correctly
@sql/05_demand_planning.sql     -- Demand planning queries
@sql/06_supplier_analytics.sql  -- Supplier analytics
@sql/07_warehouse_analytics.sql -- Warehouse analytics
@sql/08_product_analytics.sql   -- Product analytics
@sql/10_dashboard_queries.sql   -- Dashboard KPIs
```

### Connect Power BI

1. Open Power BI Desktop → Get Data → Oracle Database
2. Server: `localhost:1521/XEPDB1`
3. Import all five business views
4. Build dashboards using the view-to-page mapping documented above

---

## Technical Notes

- Sales columns in the source CSV contain accounting-style negatives `(1,234)` and commas. These are cleaned to proper numeric values during the Transform phase.
- `RETAIL_TRANSFERS` are excluded from `TOTAL_SALES` in business views because they represent inventory movement between stores, not revenue.
- Key consistency checks run on the raw data (before cleaning) to detect original inconsistencies in the source.
- The Oracle loader handles `NaN` to `None` conversion explicitly for nullable columns to ensure clean inserts.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3 |
| Data Processing | Pandas |
| Database | Oracle XE 21c |
| DB Driver | python-oracledb |
| SQL | PL/SQL, Views, Window Functions |
| Visualization | Power BI |
