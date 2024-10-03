from openai import OpenAI
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv(override=True)

def get_db_connection():
    try:
        return psycopg2.connect(
            user="postgres",
            password=os.getenv("DB_PASSWORD"),
            host="localhost",
            port="5432",
            database="store"
        )
    except Exception as e:
      print(e.with_traceback())

def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(open('table_creation.sql', 'r').read())
        conn.commit()
        cursor.close()
    except Exception as e:
        print(e.with_traceback())

def insert_starting_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(open('data_creation.sql', 'r').read())
        conn.commit()
        cursor.close()
    except Exception as e:
        print(e.with_traceback())

def get_user_input():
    return input("Enter a prompt: ")

def main():
    conn = get_db_connection()
    create_tables(conn=conn)
    insert_starting_data(conn=conn)

main()