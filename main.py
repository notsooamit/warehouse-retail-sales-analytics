from src.explore import *
from src.config import *
from src.clean import clean_dataset
from src.normalize import *
from src.oracle_loader import connect_to_oracle, load_supplier_data, load_item_data, load_sales_data


df = load_dataset()

if df is not None:
    dataset_summary(df)
    missing_values_report(df)
    distinct_value_report(df)
    duplicate_report(df)
    for column in SALES_COLUMNS:
        special_character_report(df,column)
    clean_df = clean_dataset(df)
    print("\nCleaning Completed Successfully!")
    print(clean_df.head())


    key_consistency_report(df)

    supplier_df, item_df, sales_df = normalize_dataset(clean_df)

    print("\nNormalization Complete")
    print(f"Supplier Table : {len(supplier_df)} rows")
    print(f"Item Table     : {len(item_df)} rows")
    print(f"Sales Table    : {len(sales_df)} rows")

    # Load into Oracle
    connection = connect_to_oracle()

    load_supplier_data(connection, supplier_df)
    load_item_data(connection, item_df)
    load_sales_data(connection, sales_df)

    connection.close()
    print("\nETL Pipeline Complete.")