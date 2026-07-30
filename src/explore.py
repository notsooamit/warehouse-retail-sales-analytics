import pandas as pd
import re

from src.config import CSV_PATH

def load_dataset():
    try:
        df = pd.read_csv(CSV_PATH)
        print("DATA LOADED")
        return df
    except Exception as e:
        print(f"Error loading dataset : {e}")
        return None

def dataset_summary(df):
    print("Dataset Summary")

    print(f"ROWS : {df.shape[0]}")
    print(f"COLUMNS : {df.shape[1]}")

    print("\nColumn Names")
    for column in df.columns:
        print(column)

    print("\nData Types")
    print(df.dtypes)

    print("\nMemory Usage")
    memory = df.memory_usage(deep=True).sum() / (1024 * 1024)
    print(f"{memory:.2f} MB")


def missing_values_report(df):
    print("\nMissing Values Report")
    total_rows = len(df)
    print(f"{'COLUMN':<25}{'MISSING':<15}{'PERCENTAGE'}")

    for column in df.columns:
        missing = df[column].isnull().sum()
        percentage = (missing/total_rows)*100
        print(f"{column:<25}{missing:<15}{percentage:.2f}%")

def distinct_value_report(df):
    print("\nDistinct Values Report")
    print(f"{'COLUMN':<25}{'DISTINCT'}")
    for column in df.columns:
        distinct = df[column].nunique(dropna=True)
        print(f"{column:<25}{distinct}")

def duplicate_report(df):
    print("\nDuplicate Report")
    duplicate_rows = df.duplicated().sum()
    if duplicate_rows == 0:
        print("No Duplicate Rows Found.")
    else:
        print(f"Duplicate Rows : {duplicate_rows}")

'''def special_character_report(df, column_name):
    print(f"\nSpecial Character Report : {column_name}")
    column = df[column_name].fillna("").astype(str)
    accounting_negative = column.str.contains(r"\(",regex=True).sum()
    commas = column.str.contains(",",regex=False).sum()
    empty_paranthesis =  column.str.fullmatch(r"\([^)]*,[^)]*\)").sum()
    blanks = column.str.strip().eq("").sum()
    invalid = column.str.contains(r"[^0-9(),.\-\s]", regex =True).sum()

    print(f"Accounting Negatives : {accounting_negative}")
    print(f"Comma Values         : {commas}")
    print(f"(,) Values           : {empty_paranthesis}")
    print(f"Blank Values         : {blanks}")
    print(f"Invalid Characters   : {invalid}")'''

def special_character_report(df, column_name):

    print(f"\nSpecial Character Report : {column_name}")

    column = df[column_name].fillna("").astype(str)

    has_accounting = column.str.contains(r"\(", regex=True)
    has_comma = column.str.contains(",", regex=False)

    accounting_only = (has_accounting & ~has_comma).sum()
    comma_only = (has_comma & ~has_accounting).sum()
    accounting_with_comma = (has_accounting & has_comma).sum()

    blank_values = column.str.strip().eq("").sum()

    invalid_characters = column.str.contains(
        r"[^0-9(),.\-\s]",
        regex=True
    ).sum()

    print(f"Accounting Only      : {accounting_only}")
    print(f"Comma Only           : {comma_only}")
    print(f"Accounting + Comma   : {accounting_with_comma}")
    print(f"Blank Values         : {blank_values}")
    print(f"Invalid Characters   : {invalid_characters}")


def key_consistency_report(df):

    print("\nKey Consistency Report")

    checks = [
        ("ITEM DESCRIPTION", "ITEM DESCRIPTION"),
        ("ITEM TYPE", "ITEM TYPE"),
        ("SUPPLIER", "SUPPLIER")
    ]

    for title, column in checks:

        inconsistent = (
            df.groupby("ITEM CODE")[column]
            .nunique(dropna=False)
            .gt(1)
            .sum()
        )

        print(f"ITEM CODE -> {title:<17}: {inconsistent}")

def show_key_conflicts(df, column_name, limit=5):

    conflict_codes = (
        df.groupby("ITEM CODE")[column_name]
        .nunique(dropna=False)
    )

    conflict_codes = conflict_codes[conflict_codes > 1].index

    print(f"\nITEM CODE -> {column_name} Conflicts")

    for item_code in conflict_codes[:limit]:
        print("\n" + "=" * 60)
        print(f"ITEM CODE: {item_code}")

        columns = [
            "ITEM CODE",
            "ITEM DESCRIPTION",
            "ITEM TYPE",
            "SUPPLIER",
            "YEAR",
            "MONTH"
        ]

        print(
            df[df["ITEM CODE"] == item_code][columns]
            .drop_duplicates()
            .to_string(index=False)
        )