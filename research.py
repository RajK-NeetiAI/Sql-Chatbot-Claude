import os
import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import config


def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE {db_name}")
    print(f"Database {db_name} created successfully.")


def escape_quotes(value):
    return str(value).replace("'", "''")


def create_table_from_csv(cursor, csv_file, table_name):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Create a table
    columns_with_types = ", ".join([f"{col} TEXT" for col in df.columns])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"
    cursor.execute(create_table_query)
    print(f"Table {table_name} created successfully.")

    # Then in your insertion loop:
    for index, row in df.iterrows():
        columns = ', '.join(df.columns)
        values = ', '.join([f"'{escape_quotes(value)}'" for value in row])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        cursor.execute(insert_query)


def main():
    # Connection parameters - update these with your details
    user = config.POSTGRES_USER
    password = config.POSTGRES_PASSWORD
    host = config.POSTGRES_HOST

    # Connect to PostgreSQL server
    conn = psycopg2.connect(dbname='postgres', user=user,
                            password=password, host=host)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    # Create a new database
    db_name = 'new_database'
    create_database(cursor, db_name)

    # Connect to the new database
    conn.close()
    conn = psycopg2.connect(dbname=db_name, user=user,
                            password=password, host=host)
    cursor = conn.cursor()

    # Path to the directory containing CSV files
    path_to_csv_directory = 'Tables/'

    # Process each CSV file
    for csv_file in os.listdir(path_to_csv_directory):
        if csv_file.endswith('.csv'):
            table_name = os.path.splitext(csv_file)[0]
            create_table_from_csv(cursor, os.path.join(
                path_to_csv_directory, csv_file), table_name)

    # Close the connection
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
