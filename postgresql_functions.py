
import decimal
import json
import datetime
import os

# Importing psycopg2 and pool module
import psycopg2
from psycopg2 import pool

import config


def connect_to_postgresql_pool() -> psycopg2.pool.SimpleConnectionPool | None:
    '''Create a PostgreSQL connection pool
    '''
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=5,
            host=config.POSTGRES_HOST,
            database=config.POSTGRES_DB_NAME,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD
        )
        return connection_pool
    except psycopg2.DatabaseError as e:
        print(f"Error creating PostgreSQL connection pool: {e}")
        return None


def get_postgresql_pooled_cnx() -> psycopg2.extensions.connection | None:
    '''Get a new PostgreSQL connection from the connection pool
    '''
    pool = connect_to_postgresql_pool()
    if not pool:
        return None
    try:
        cnx = pool.getconn()
        return cnx
    except psycopg2.DatabaseError as e:
        print(f"Error getting connection from pool: {e}")
        return None


def close_postgresql_cnx(cnx) -> None:
    '''Release a PostgreSQL connection back to the pool
    '''
    try:
        pool.putconn(cnx)
    except psycopg2.DatabaseError as e:
        print(f"Error putting connection back to pool: {e}")


def execute_query(cnx, query, params=None) -> list:
    '''Execute a query and return the results
    '''
    try:
        with cnx.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except psycopg2.DatabaseError as e:
        print(f"Error executing query: {e}")
        return []
