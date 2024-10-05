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

def zero_shot_single_domain(prompt):
    db_schema = open('table_creation.sql', 'r').read()
    task_instruction = 'Provide valid PostgreSQL syntax to answer the following question for the above database schema'

    question = f'Question: {prompt}'

    model_input = f'{db_schema}\n\n{task_instruction}\n\n{question}'

    return model_input

def one_shot_single_domain(prompt):
    db_schema = open('table_creation.sql', 'r').read()
    task_instruction = 'Provide valid PostgreSQL syntax to answer the following question for the above database schema'

    example_question = "Example question: How much total has Alice spent all time?"
    example_response = "Example response: SELECT SUM(Price * Quantity) AS TotalSpent FROM Users JOIN Orders ON Users.UserID = Orders.UserID JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID JOIN Products ON OrderDetails.ProductID = Products.ProductID WHERE Users.FirstName = 'Alice';"
    
    question = f'Question: {prompt}'

    model_input = f'{db_schema}\n\n{task_instruction}\n\n{example_question}\n\n{example_response}\n\n{question}'

    return model_input

def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(e.with_traceback())


def main():
    conn = get_db_connection()
    create_tables(conn=conn)
    insert_starting_data(conn=conn)

    openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    user_input = get_user_input()
    zero_shot_model_input = zero_shot_single_domain(user_input)
    one_shot_model_input = one_shot_single_domain(user_input)

    print('model input:', one_shot_model_input)

    completions = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": one_shot_model_input
            }
        ]
    )

    resulting_query = completions.choices[0].message.content

    print('Model response query:', resulting_query)

    query_result = execute_query(conn, resulting_query)
    
    print('Result of running model query:', query_result)
    
    

main()