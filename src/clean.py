import pandas as pd
from src.config import SALES_COLUMNS


def clean_sales_column(df, column_name):
    """
    Clean a single sales column.
    """

    df[column_name] = (
        df[column_name]
        .fillna("")
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("(", "-", regex=False)
        .str.replace(")", "", regex=False)
    )

    df[column_name] = pd.to_numeric(
        df[column_name],
        errors="coerce"
    )

    return df


def clean_sales_columns(df):
    """
    Clean all sales columns.
    """

    for column in SALES_COLUMNS:
        df = clean_sales_column(df, column)

    return df


def validate_sales_columns(df):
    """
    Validate cleaned sales columns.
    """

    print("\nSales Column Validation")

    for column in SALES_COLUMNS:

        print(f"\n{column}")

        # Check data type
        if pd.api.types.is_numeric_dtype(df[column]):
            print("Data Type        : PASS")
        else:
            print("Data Type        : FAIL")

        # Check missing values
        print(f"Missing Values   : {df[column].isna().sum()}")

        # Check for commas
        comma_count = df[column].astype(str).str.contains(",", regex=False).sum()
        print(f"Comma Remaining  : {comma_count}")

        # Check for opening brackets
        bracket_count = df[column].astype(str).str.contains(r"\(", regex=True).sum()
        print(f"Bracket Remaining: {bracket_count}")


def clean_dataset(df):
    """
    Main cleaning pipeline.
    """

    df = clean_sales_columns(df)

    validate_sales_columns(df)

    return df