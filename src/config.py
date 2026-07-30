CSV_PATH = "data/sales.csv"

SALES_COLUMNS = [
    "RETAIL SALES",
    "RETAIL TRANSFERS",
    "WAREHOUSE SALES"
]

TEXT_COLUMN = [
    "SUPPLIER",
    "ITEM CODE",
    "ITEM DESCRIPTION",
    "ITEM TYPE"
]

DATE_COLUMNS = [
    "YEAR",
    "MONTHS"
]


# Oracle Database Configuration

DB_USER = "sales_etl"
DB_PASSWORD = "sales123"
DB_HOST = "localhost"
DB_PORT = 1521
DB_SERVICE = "XEPDB1"