import pandas as pd


def create_supplier_table(df):

    supplier_df = (
        df[["SUPPLIER"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    supplier_df.insert(
        0,
        "SUPPLIER_ID",
        supplier_df.index + 1
    )

    supplier_df.rename(
        columns={
            "SUPPLIER": "SUPPLIER_NAME"
        },
        inplace=True
    )

    return supplier_df


def create_item_table(df):

    item_df = (
        df[
            [
                "ITEM CODE",
                "ITEM DESCRIPTION",
                "ITEM TYPE"
            ]
        ]
        .drop_duplicates(subset=["ITEM CODE"])
        .reset_index(drop=True)
    )

    item_df.rename(
        columns={
            "ITEM CODE": "ITEM_CODE",
            "ITEM DESCRIPTION": "ITEM_DESCRIPTION",
            "ITEM TYPE": "ITEM_TYPE"
        },
        inplace=True
    )

    return item_df


def create_sales_table(df, supplier_df):

    sales_df = (
        df.merge(
            supplier_df,
            left_on="SUPPLIER",
            right_on="SUPPLIER_NAME",
            how="left"
        )
    )

    sales_df = sales_df[
        [
            "YEAR",
            "MONTH",
            "ITEM CODE",
            "SUPPLIER_ID",
            "RETAIL SALES",
            "RETAIL TRANSFERS",
            "WAREHOUSE SALES"
        ]
    ]

    sales_df.rename(
        columns={
            "ITEM CODE": "ITEM_CODE",
            "RETAIL SALES": "RETAIL_SALES",
            "RETAIL TRANSFERS": "RETAIL_TRANSFERS",
            "WAREHOUSE SALES": "WAREHOUSE_SALES"
        },
        inplace=True
    )

    return sales_df

def validate_normalization(supplier_df, item_df, sales_df):

    print("\nNormalization Validation")

    print(f"\nSupplier Rows : {len(supplier_df)}")
    print(f"Item Rows     : {len(item_df)}")
    print(f"Sales Rows    : {len(sales_df)}")

    print("\nDuplicate Primary Keys")

    print(
        f"SUPPLIER_ID : {supplier_df['SUPPLIER_ID'].duplicated().sum()}"
    )

    print(
        f"ITEM_CODE   : {item_df['ITEM_CODE'].duplicated().sum()}"
    )

    print("\nMissing Foreign Keys")

    print(
        f"SUPPLIER_ID : {sales_df['SUPPLIER_ID'].isna().sum()}"
    )

    print(
        f"ITEM_CODE   : {sales_df['ITEM_CODE'].isna().sum()}"
    )

def normalize_dataset(df):

    supplier_df = create_supplier_table(df)

    item_df = create_item_table(df)

    sales_df = create_sales_table(df, supplier_df)

    validate_normalization(
        supplier_df,
        item_df,
        sales_df
    )

    return supplier_df, item_df, sales_df