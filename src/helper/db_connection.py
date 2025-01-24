import os
import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return conn


'''
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        port=50444,
        dbname='DIP',
        user='AbgWatch_admin',
        password='adafg-trastr-8090'
    )
    return conn
'''