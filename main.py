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
      print(e)

def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(open('table_creation.sql', 'r').read())
        cursor.close()
    except Exception as e:
        print(e)

def get_user_input():
    return input("Enter a prompt: ")

def main():
    conn = get_db_connection()
    create_tables(conn=conn)

    # run the show table command
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
    tables = cursor.fetchall()
    print(tables)
    cursor.close()

main()