import os
import psycopg2


def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database using environment variables
    Returns:
        A connection object to the PostgreSQL database
    Raises:
        psycopg2.OperationalError: If there is an issue with establishing the database connection
    """
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return conn
