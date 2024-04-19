from psycopg2 import pool
import psycopg2
import psycopg2.extras
import psycopg2.pool

import config


# Global pool variable
global_connection_pool = None


def connect_to_postgresql_pool() -> psycopg2.pool.SimpleConnectionPool | None:
    '''Create or retrieve a PostgreSQL connection pool as a singleton.'''
    global global_connection_pool
    if global_connection_pool is None:
        try:
            global_connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=5,
                host=config.POSTGRES_HOST,
                database=config.POSTGRES_DB_NAME,
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD
            )
        except psycopg2.DatabaseError as e:
            print(f"Error creating PostgreSQL connection pool: {e}")
            global_connection_pool = None
    return global_connection_pool


def get_postgresql_pooled_cnx() -> psycopg2.extensions.connection | None:
    '''Get a new PostgreSQL connection from the connection pool
    '''
    pool = connect_to_postgresql_pool()
    if not pool:
        return None
    try:
        cnx = pool.getconn()
        return cnx
    except Exception as e:
        print(f"Error getting connection from pool: {e}")
        return None


def close_postgresql_cnx(cnx: psycopg2.extensions.connection) -> None:
    '''Release a PostgreSQL connection back to the pool
    '''
    pool = connect_to_postgresql_pool()
    if pool is not None and cnx is not None:
        try:
            pool.putconn(cnx)
        except psycopg2.DatabaseError as e:
            print(f"Error putting connection back to pool: {e}")


def get_table_names() -> list[str]:
    """Return a list of table names."""
    cnx = get_postgresql_pooled_cnx()
    cursor = cnx.cursor()
    table_names = []
    cursor.execute(
        f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{config.POSTGRES_DB_NAME}';")
    results = cursor.fetchall()
    print(results)
    for table in results:
        table_names.append(table[0])
    cursor.close()
    close_postgresql_cnx(cnx)
    return table_names


def get_column_names_for_data_definitions(table_name: str) -> list[str]:
    """Return a list of column names."""
    cnx = get_postgresql_pooled_cnx()
    cursor = cnx.cursor()
    column_names = []
    cursor.execute(
        f"SELECT `COLUMN_NAME`, `DATA_TYPE` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='{config.POSTGRES_DB_NAME}' AND `TABLE_NAME`='{table_name}';")
    for col in cursor:
        column_names.append(col)
    cursor.close()
    close_postgresql_cnx(cnx)
    return column_names


def get_column_names(table_name: str) -> list[str]:
    """Return a list of column names."""
    cnx = get_postgresql_pooled_cnx()
    cursor = cnx.cursor()
    column_names = []
    cursor.execute(
        f"SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='{config.POSTGRES_DB_NAME}' AND `TABLE_NAME`='{table_name}';")
    for col in cursor:
        column_names.append(col[0])
    cursor.close()
    close_postgresql_cnx(cnx)
    return column_names


def get_database_info() -> dict:
    """Return a list of dicts containing the table name and columns for each table in the database."""
    cnx = get_postgresql_pooled_cnx()
    cursor = cnx.cursor()
    table_dicts = []
    for table_name in get_table_names():
        columns_names = get_column_names(table_name)
        table_dicts.append(
            {"table_name": table_name, "column_names": columns_names})
    cursor.close()
    close_postgresql_cnx(cnx)
    return table_dicts


def get_database_schema_string() -> str:
    '''Get database schema as a string
    '''
    database_schema_dict = get_database_info()
    database_schema_string = "\n".join(
        [
            f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
            for table in database_schema_dict
        ]
    )
    return database_schema_string


def ask_database(query: str) -> str:
    """Function to query SQLite database with a provided SQL query."""
    cnx = get_postgresql_pooled_cnx()
    results = []
    if cnx == None:
        return results
    try:
        cursor = cnx.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query)
        results = cursor.fetchall()
        print(results)
    except Exception as e:
        print(f'Error at ask_database -> {e}')
    finally:
        close_postgresql_cnx(cnx)
    return results


def execute_query(cnx, query) -> list:
    '''Execute a query and return the results
    '''
    try:
        with cnx.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        return []


print(ask_database("SELECT * FROM information_schema.tables WHERE table_schema = 'sql_chatbot'"))
