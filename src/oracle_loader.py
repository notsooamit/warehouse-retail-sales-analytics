import oracledb
import pandas as pd
from src.config import (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_SERVICE,
)

def connect_to_oracle():
    """
    Create and return an Oracle database connection.
    """

    connection = oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        service_name=DB_SERVICE,
    )

    print("Connected to Oracle Database.")

    return connection

def load_supplier_data(connection, supplier_df):

    cursor = connection.cursor()

    sql = """
        INSERT INTO SUPPLIER (
            SUPPLIER_ID,
            SUPPLIER_NAME
        )
        VALUES (:1, :2)
    """

    data = []

    for _, row in supplier_df.iterrows():

        supplier_id = int(row["SUPPLIER_ID"])

        supplier_name = row["SUPPLIER_NAME"]

        if pd.isna(supplier_name):
            supplier_name = None

        data.append((supplier_id, supplier_name))

    cursor.executemany(sql, data)

    connection.commit()

    print(f"{cursor.rowcount} rows inserted into SUPPLIER.")

    cursor.close()

def load_item_data(connection, item_df):

    cursor = connection.cursor()

    sql = """
        INSERT INTO ITEM (
            ITEM_CODE,
            ITEM_DESCRIPTION,
            ITEM_TYPE
        )
        VALUES (:1, :2, :3)
    """

    data = []

    for _, row in item_df.iterrows():

        item_code = row["ITEM_CODE"]

        item_description = row["ITEM_DESCRIPTION"]
        if pd.isna(item_description):
            item_description = None

        item_type = row["ITEM_TYPE"]
        if pd.isna(item_type):
            item_type = None

        data.append((
            item_code,
            item_description,
            item_type
        ))

    cursor.executemany(sql, data)

    connection.commit()

    print(f"{cursor.rowcount} rows inserted into ITEM.")

    cursor.close()


def load_sales_data(connection, sales_df):

    cursor = connection.cursor()

    sql = """
        INSERT INTO SALES (
            YEAR,
            MONTH,
            ITEM_CODE,
            SUPPLIER_ID,
            RETAIL_SALES,
            RETAIL_TRANSFERS,
            WAREHOUSE_SALES
        )
        VALUES (:1, :2, :3, :4, :5, :6, :7)
    """

    data = []

    for _, row in sales_df.iterrows():

        retail_sales = row["RETAIL_SALES"]
        if pd.isna(retail_sales):
            retail_sales = None

        retail_transfers = row["RETAIL_TRANSFERS"]
        if pd.isna(retail_transfers):
            retail_transfers = None

        warehouse_sales = row["WAREHOUSE_SALES"]
        if pd.isna(warehouse_sales):
            warehouse_sales = None

        data.append((
            int(row["YEAR"]),
            int(row["MONTH"]),
            row["ITEM_CODE"],
            int(row["SUPPLIER_ID"]),
            retail_sales,
            retail_transfers,
            warehouse_sales
        ))

    cursor.executemany(sql, data)

    connection.commit()

    print(f"{cursor.rowcount} rows inserted into SALES.")

    cursor.close()